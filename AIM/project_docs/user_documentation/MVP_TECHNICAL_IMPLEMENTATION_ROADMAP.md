# AIM MVP Implementation Roadmap: Technical Specifications and Code Examples

## 🛠️ **Technical Implementation Strategy**

This document provides detailed technical specifications, code examples, and implementation guidelines for the AIM MVP development. It serves as a technical companion to the comprehensive requirements analysis, focusing on practical implementation details.

---

## 🏗️ **Architecture Overview**

### **System Architecture Diagram**
```
┌─────────────────────────────────────────────────────────────┐
│                    AIM MVP Architecture                      │
├─────────────────┬─────────────────┬─────────────────────────┤
│   Presentation  │   Business      │    Data Layer           │
│     Layer       │    Logic        │                         │
├─────────────────┼─────────────────┼─────────────────────────┤
│ • tkinter GUI   │ • Field Mapper  │ • SQLite Database       │
│ • Dialog System │ • Data Validator│ • File Manager          │
│ • Progress UI   │ • Excel Processor│ • Cache Layer          │
│ • Status Updates│ • AI Engine     │ • Backup System         │
└─────────────────┴─────────────────┴─────────────────────────┘
```

### **Core Components Structure**
```
AIM/
├── src/                          # Core business logic
│   ├── aim_processor.py         # Main processing engine
│   ├── calculators/             # Future calculator modules
│   ├── config/                  # Configuration management
│   ├── mappers/                 # Field mapping logic
│   ├── parsers/                 # Data parsing utilities
│   └── validators/              # Data validation engine
├── common/                      # Shared utilities
│   ├── ui_utils.py             # UI helper functions
│   ├── database_manager.py     # Database operations
│   ├── file_manager.py         # File handling utilities
│   └── ai_engine.py            # AI processing (MVP Phase 2)
├── models/                     # AI models and weights
├── config/                     # Configuration files
├── data/                       # Sample data and templates
└── tests/                      # Test suite
```

---

## 🔧 **Phase 1 Implementation: Core MVP (Current State)**

### **Database Schema Design**

```sql
-- SQLite Database Schema for AIM MVP
CREATE TABLE IF NOT EXISTS user_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    product_type TEXT NOT NULL CHECK(product_type IN ('life', 'annuity')),
    data_hash TEXT UNIQUE NOT NULL,
    json_data TEXT NOT NULL,
    field_mappings TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    validation_status TEXT DEFAULT 'pending',
    quality_score REAL DEFAULT 0.0
);

CREATE TABLE IF NOT EXISTS field_mapping_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_field TEXT NOT NULL,
    target_field TEXT NOT NULL,
    confidence_score REAL DEFAULT 0.0,
    user_approved BOOLEAN DEFAULT FALSE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id TEXT
);

CREATE TABLE IF NOT EXISTS processing_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation_type TEXT NOT NULL,
    operation_details TEXT,
    status TEXT CHECK(status IN ('success', 'warning', 'error')),
    error_message TEXT,
    processing_time_ms INTEGER,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance optimization
CREATE INDEX idx_user_data_hash ON user_data(data_hash);
CREATE INDEX idx_field_mapping_source ON field_mapping_history(source_field);
CREATE INDEX idx_processing_logs_date ON processing_logs(created_date);
CREATE INDEX idx_user_data_product ON user_data(product_type);
```

### **Enhanced Database Manager Implementation**

```python
import sqlite3
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging

class EnhancedDatabaseManager:
    def __init__(self, db_path: str = "aim_data.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.init_database()
    
    def init_database(self):
        """Initialize database with enhanced schema"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.executescript("""
                    -- Main user data table
                    CREATE TABLE IF NOT EXISTS user_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        product_type TEXT NOT NULL CHECK(product_type IN ('life', 'annuity')),
                        data_hash TEXT UNIQUE NOT NULL,
                        json_data TEXT NOT NULL,
                        field_mappings TEXT,
                        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        validation_status TEXT DEFAULT 'pending',
                        quality_score REAL DEFAULT 0.0,
                        file_source TEXT,
                        processing_notes TEXT
                    );
                    
                    -- Field mapping history for AI learning
                    CREATE TABLE IF NOT EXISTS field_mapping_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        source_field TEXT NOT NULL,
                        target_field TEXT NOT NULL,
                        product_type TEXT NOT NULL,
                        confidence_score REAL DEFAULT 0.0,
                        user_approved BOOLEAN DEFAULT FALSE,
                        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        user_id TEXT,
                        mapping_context TEXT
                    );
                    
                    -- Processing activity logs
                    CREATE TABLE IF NOT EXISTS processing_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        operation_type TEXT NOT NULL,
                        operation_details TEXT,
                        status TEXT CHECK(status IN ('success', 'warning', 'error')),
                        error_message TEXT,
                        processing_time_ms INTEGER,
                        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        user_session TEXT
                    );
                    
                    -- User preferences and settings
                    CREATE TABLE IF NOT EXISTS user_preferences (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        preference_key TEXT UNIQUE NOT NULL,
                        preference_value TEXT NOT NULL,
                        updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                    
                    -- Performance indexes
                    CREATE INDEX IF NOT EXISTS idx_user_data_hash ON user_data(data_hash);
                    CREATE INDEX IF NOT EXISTS idx_field_mapping_source ON field_mapping_history(source_field);
                    CREATE INDEX IF NOT EXISTS idx_processing_logs_date ON processing_logs(created_date);
                    CREATE INDEX IF NOT EXISTS idx_user_data_product ON user_data(product_type);
                """)
                self.logger.info("Database initialized successfully")
        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")
            raise
    
    def store_data_with_validation(self, name: str, product_type: str, json_data: Dict, 
                                 field_mappings: Optional[Dict] = None, 
                                 file_source: Optional[str] = None) -> Dict[str, Any]:
        """Store data with comprehensive validation and quality scoring"""
        try:
            # Calculate data hash for duplicate detection
            data_str = json.dumps(json_data, sort_keys=True)
            data_hash = hashlib.md5(data_str.encode()).hexdigest()
            
            # Validate data quality
            quality_result = self.calculate_quality_score(json_data)
            
            # Check for duplicates
            if self.check_duplicate_hash(data_hash):
                return {
                    'success': False,
                    'error': 'duplicate',
                    'message': 'Data already exists in database',
                    'existing_record': self.get_record_by_hash(data_hash)
                }
            
            # Store the record
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO user_data 
                    (name, product_type, data_hash, json_data, field_mappings, 
                     validation_status, quality_score, file_source, processing_notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    name, product_type, data_hash, json.dumps(json_data),
                    json.dumps(field_mappings) if field_mappings else None,
                    quality_result['status'], quality_result['score'],
                    file_source, quality_result['notes']
                ))
                
                record_id = cursor.lastrowid
                
                # Log the operation
                self.log_operation(
                    operation_type='data_store',
                    operation_details=f'Stored record for {name}',
                    status='success',
                    processing_time_ms=0  # Could be measured
                )
                
                return {
                    'success': True,
                    'record_id': record_id,
                    'quality_score': quality_result['score'],
                    'validation_status': quality_result['status']
                }
                
        except Exception as e:
            self.logger.error(f"Error storing data: {e}")
            self.log_operation(
                operation_type='data_store',
                operation_details=f'Failed to store record for {name}',
                status='error',
                error_message=str(e)
            )
            return {
                'success': False,
                'error': 'storage_error',
                'message': str(e)
            }
    
    def calculate_quality_score(self, json_data: Dict) -> Dict[str, Any]:
        """Calculate data quality score based on various factors"""
        score = 0.0
        max_score = 100.0
        notes = []
        
        # Check for required fields
        required_fields = ['policy_number', 'product_type', 'effective_date']
        present_required = sum(1 for field in required_fields if field in json_data)
        score += (present_required / len(required_fields)) * 30
        
        # Check data completeness
        total_fields = len(json_data)
        non_empty_fields = sum(1 for v in json_data.values() if v is not None and str(v).strip())
        completeness = non_empty_fields / total_fields if total_fields > 0 else 0
        score += completeness * 25
        
        # Check data format consistency
        format_score = self.check_data_formats(json_data)
        score += format_score * 25
        
        # Check for suspicious values
        anomaly_score = self.detect_data_anomalies(json_data)
        score += anomaly_score * 20
        
        # Determine validation status
        if score >= 80:
            status = 'validated'
        elif score >= 60:
            status = 'warning'
            notes.append(f"Quality score below 80%: {score:.1f}")
        else:
            status = 'needs_review'
            notes.append(f"Low quality score: {score:.1f}")
        
        return {
            'score': round(score, 2),
            'status': status,
            'notes': '; '.join(notes)
        }
    
    def check_data_formats(self, json_data: Dict) -> float:
        """Check data format consistency"""
        format_score = 1.0
        
        # Date format checks
        date_fields = ['effective_date', 'birth_date', 'issue_date']
        for field in date_fields:
            if field in json_data:
                if not self.is_valid_date_format(json_data[field]):
                    format_score -= 0.2
        
        # Numeric format checks
        numeric_fields = ['face_amount', 'premium', 'age']
        for field in numeric_fields:
            if field in json_data:
                if not self.is_valid_numeric(json_data[field]):
                    format_score -= 0.2
        
        return max(0.0, format_score)
    
    def detect_data_anomalies(self, json_data: Dict) -> float:
        """Detect potential data anomalies"""
        anomaly_score = 1.0
        
        # Age validation
        if 'age' in json_data:
            try:
                age = float(json_data['age'])
                if age < 0 or age > 120:
                    anomaly_score -= 0.3
            except:
                anomaly_score -= 0.3
        
        # Amount validation
        if 'face_amount' in json_data:
            try:
                amount = float(json_data['face_amount'])
                if amount <= 0 or amount > 100000000:  # $100M limit
                    anomaly_score -= 0.3
            except:
                anomaly_score -= 0.3
        
        return max(0.0, anomaly_score)
    
    def store_field_mapping_feedback(self, source_field: str, target_field: str, 
                                   product_type: str, user_approved: bool, 
                                   confidence_score: float = 0.0) -> bool:
        """Store field mapping feedback for AI learning"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO field_mapping_history
                    (source_field, target_field, product_type, confidence_score, 
                     user_approved, mapping_context)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    source_field, target_field, product_type, 
                    confidence_score, user_approved, 
                    json.dumps({'timestamp': datetime.now().isoformat()})
                ))
                return True
        except Exception as e:
            self.logger.error(f"Error storing field mapping feedback: {e}")
            return False
    
    def get_field_mapping_history(self, product_type: Optional[str] = None) -> List[Dict]:
        """Get field mapping history for AI training"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if product_type:
                    cursor.execute("""
                        SELECT source_field, target_field, confidence_score, user_approved
                        FROM field_mapping_history 
                        WHERE product_type = ?
                        ORDER BY created_date DESC
                    """, (product_type,))
                else:
                    cursor.execute("""
                        SELECT source_field, target_field, confidence_score, user_approved
                        FROM field_mapping_history 
                        ORDER BY created_date DESC
                    """)
                
                rows = cursor.fetchall()
                return [
                    {
                        'source_field': row[0],
                        'target_field': row[1],
                        'confidence_score': row[2],
                        'user_approved': bool(row[3])
                    }
                    for row in rows
                ]
        except Exception as e:
            self.logger.error(f"Error retrieving field mapping history: {e}")
            return []
    
    def get_analytics_data(self) -> Dict[str, Any]:
        """Get comprehensive analytics data for reporting"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Basic statistics
                cursor.execute("SELECT COUNT(*) FROM user_data")
                total_records = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT product_type, COUNT(*) 
                    FROM user_data 
                    GROUP BY product_type
                """)
                product_distribution = dict(cursor.fetchall())
                
                cursor.execute("""
                    SELECT AVG(quality_score), MIN(quality_score), MAX(quality_score)
                    FROM user_data
                """)
                quality_stats = cursor.fetchone()
                
                cursor.execute("""
                    SELECT validation_status, COUNT(*)
                    FROM user_data
                    GROUP BY validation_status
                """)
                validation_distribution = dict(cursor.fetchall())
                
                # Processing statistics
                cursor.execute("""
                    SELECT operation_type, status, COUNT(*)
                    FROM processing_logs
                    WHERE created_date >= datetime('now', '-30 days')
                    GROUP BY operation_type, status
                """)
                processing_stats = cursor.fetchall()
                
                return {
                    'total_records': total_records,
                    'product_distribution': product_distribution,
                    'quality_stats': {
                        'average': quality_stats[0] if quality_stats[0] else 0,
                        'minimum': quality_stats[1] if quality_stats[1] else 0,
                        'maximum': quality_stats[2] if quality_stats[2] else 0
                    },
                    'validation_distribution': validation_distribution,
                    'processing_stats': processing_stats,
                    'generated_date': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Error retrieving analytics data: {e}")
            return {}
```

---

## 🤖 **Phase 2 Implementation: AI Engine Integration**

### **AI Engine Core Implementation**

```python
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import IsolationForest
from typing import List, Dict, Tuple, Optional
import joblib
import json
from datetime import datetime
import logging

class AIEngine:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.logger = logging.getLogger(__name__)
        self.model_name = model_name
        self.embedding_model = None
        self.anomaly_detector = None
        self.field_cache = {}
        self.is_initialized = False
        
        self.initialize_models()
    
    def initialize_models(self):
        """Initialize AI models with error handling"""
        try:
            # Initialize sentence transformer for field similarity
            self.embedding_model = SentenceTransformer(self.model_name)
            self.logger.info(f"Loaded embedding model: {self.model_name}")
            
            # Load pre-trained anomaly detector if available
            try:
                self.anomaly_detector = joblib.load('models/anomaly_detector.pkl')
                self.logger.info("Loaded pre-trained anomaly detector")
            except FileNotFoundError:
                self.logger.info("No pre-trained anomaly detector found, will create new one")
            
            self.is_initialized = True
            
        except Exception as e:
            self.logger.error(f"Error initializing AI models: {e}")
            self.is_initialized = False
    
    def get_field_suggestions(self, source_field: str, target_fields: List[str], 
                             product_type: str = 'life', top_k: int = 3) -> List[Dict]:
        """Get AI-powered field mapping suggestions"""
        if not self.is_initialized:
            return self.get_fallback_suggestions(source_field, target_fields, top_k)
        
        try:
            # Get or compute source field embedding
            source_embedding = self.get_field_embedding(source_field)
            
            # Get or compute target field embeddings
            target_embeddings = [self.get_field_embedding(field) for field in target_fields]
            
            # Calculate similarities
            similarities = cosine_similarity([source_embedding], target_embeddings)[0]
            
            # Get top-k suggestions
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            suggestions = []
            for idx in top_indices:
                confidence = float(similarities[idx])
                
                # Apply business rules to adjust confidence
                adjusted_confidence = self.apply_business_rules(
                    source_field, target_fields[idx], confidence, product_type
                )
                
                suggestions.append({
                    'target_field': target_fields[idx],
                    'confidence': adjusted_confidence,
                    'similarity_score': confidence,
                    'reasoning': self.generate_reasoning(source_field, target_fields[idx]),
                    'business_rule_applied': adjusted_confidence != confidence
                })
            
            return suggestions
            
        except Exception as e:
            self.logger.error(f"Error generating AI suggestions: {e}")
            return self.get_fallback_suggestions(source_field, target_fields, top_k)
    
    def get_field_embedding(self, field_name: str) -> np.ndarray:
        """Get or compute field embedding with caching"""
        cache_key = field_name.lower().strip()
        
        if cache_key in self.field_cache:
            return self.field_cache[cache_key]
        
        # Preprocess field name for better embeddings
        processed_field = self.preprocess_field_name(field_name)
        
        # Generate embedding
        embedding = self.embedding_model.encode([processed_field])[0]
        
        # Cache the embedding
        self.field_cache[cache_key] = embedding
        
        return embedding
    
    def preprocess_field_name(self, field_name: str) -> str:
        """Preprocess field name for better semantic understanding"""
        # Convert camelCase and snake_case to space-separated words
        import re
        
        # Handle camelCase
        field_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', field_name)
        
        # Handle snake_case and kebab-case
        field_name = field_name.replace('_', ' ').replace('-', ' ')
        
        # Clean up extra spaces
        field_name = ' '.join(field_name.split())
        
        return field_name.lower()
    
    def apply_business_rules(self, source_field: str, target_field: str, 
                           confidence: float, product_type: str) -> float:
        """Apply business-specific rules to adjust confidence scores"""
        adjusted_confidence = confidence
        
        # Product-specific field boosting
        product_boost_rules = {
            'life': {
                'face_amount': ['coverage_amount', 'death_benefit', 'benefit_amount'],
                'premium': ['annual_premium', 'monthly_premium', 'premium_amount'],
                'age': ['issue_age', 'attained_age', 'current_age']
            },
            'annuity': {
                'account_value': ['cash_value', 'accumulation_value', 'contract_value'],
                'withdrawal': ['surrender_amount', 'partial_withdrawal', 'distribution'],
                'rider': ['benefit_rider', 'living_benefit', 'death_benefit_rider']
            }
        }
        
        # Apply boost if target field is in product-specific high-confidence mappings
        if product_type in product_boost_rules:
            for key_field, related_fields in product_boost_rules[product_type].items():
                if key_field.lower() in source_field.lower():
                    for related_field in related_fields:
                        if related_field.lower() in target_field.lower():
                            adjusted_confidence = min(1.0, confidence * 1.2)
                            break
        
        # Exact match bonus
        if source_field.lower() == target_field.lower():
            adjusted_confidence = min(1.0, confidence * 1.5)
        
        # Penalize obviously wrong mappings
        wrong_mappings = [
            ('date', 'amount'), ('amount', 'date'), ('name', 'number'), 
            ('number', 'name'), ('age', 'amount'), ('amount', 'age')
        ]
        
        for wrong_source, wrong_target in wrong_mappings:
            if (wrong_source in source_field.lower() and wrong_target in target_field.lower()) or \
               (wrong_target in source_field.lower() and wrong_source in target_field.lower()):
                adjusted_confidence *= 0.5
                break
        
        return round(adjusted_confidence, 3)
    
    def generate_reasoning(self, source_field: str, target_field: str) -> str:
        """Generate human-readable reasoning for field mapping suggestion"""
        source_lower = source_field.lower()
        target_lower = target_field.lower()
        
        # Exact match
        if source_lower == target_lower:
            return "Exact field name match"
        
        # Substring match
        if source_lower in target_lower or target_lower in source_lower:
            return "Field names contain common terms"
        
        # Semantic similarity
        common_terms = set(source_lower.split()) & set(target_lower.split())
        if common_terms:
            return f"Shared terms: {', '.join(common_terms)}"
        
        # Pattern matching
        if any(term in source_lower for term in ['date', 'time']) and \
           any(term in target_lower for term in ['date', 'time']):
            return "Both fields appear to be date/time related"
        
        if any(term in source_lower for term in ['amount', 'value', 'money']) and \
           any(term in target_lower for term in ['amount', 'value', 'money']):
            return "Both fields appear to be monetary values"
        
        return "Semantic similarity based on AI analysis"
    
    def get_fallback_suggestions(self, source_field: str, target_fields: List[str], 
                               top_k: int) -> List[Dict]:
        """Provide rule-based suggestions when AI is unavailable"""
        suggestions = []
        source_lower = source_field.lower()
        
        # Simple string similarity scoring
        for target_field in target_fields:
            target_lower = target_field.lower()
            
            # Calculate simple similarity score
            if source_lower == target_lower:
                score = 1.0
            elif source_lower in target_lower or target_lower in source_lower:
                score = 0.8
            else:
                # Count common words
                source_words = set(source_lower.split('_'))
                target_words = set(target_lower.split('_'))
                common_words = source_words & target_words
                if common_words:
                    score = len(common_words) / max(len(source_words), len(target_words))
                else:
                    score = 0.1
            
            suggestions.append({
                'target_field': target_field,
                'confidence': score,
                'similarity_score': score,
                'reasoning': 'Rule-based matching (AI unavailable)',
                'business_rule_applied': False
            })
        
        # Sort by confidence and return top-k
        suggestions.sort(key=lambda x: x['confidence'], reverse=True)
        return suggestions[:top_k]
    
    def detect_anomalies(self, record_data: Dict) -> Dict[str, Any]:
        """Detect data anomalies using AI"""
        if not self.anomaly_detector:
            return self.rule_based_anomaly_detection(record_data)
        
        try:
            # Convert record to feature vector
            features = self.extract_anomaly_features(record_data)
            
            # Predict anomaly
            anomaly_score = self.anomaly_detector.decision_function([features])[0]
            is_anomaly = self.anomaly_detector.predict([features])[0] == -1
            
            return {
                'is_anomaly': is_anomaly,
                'anomaly_score': float(anomaly_score),
                'confidence': min(1.0, abs(anomaly_score)),
                'method': 'ai_isolation_forest'
            }
            
        except Exception as e:
            self.logger.error(f"Error in AI anomaly detection: {e}")
            return self.rule_based_anomaly_detection(record_data)
    
    def extract_anomaly_features(self, record_data: Dict) -> List[float]:
        """Extract numerical features for anomaly detection"""
        features = []
        
        # Age feature
        if 'age' in record_data:
            try:
                age = float(record_data['age'])
                features.extend([age, age**2])  # Age and age squared
            except:
                features.extend([0.0, 0.0])
        else:
            features.extend([0.0, 0.0])
        
        # Amount features
        amount_fields = ['face_amount', 'premium', 'cash_value', 'account_value']
        for field in amount_fields:
            if field in record_data:
                try:
                    amount = float(record_data[field])
                    features.append(np.log1p(amount))  # Log-transformed amount
                except:
                    features.append(0.0)
            else:
                features.append(0.0)
        
        # Categorical features (encoded as 0/1)
        categorical_fields = ['gender', 'smoking_status', 'state']
        for field in categorical_fields:
            features.append(1.0 if field in record_data and record_data[field] else 0.0)
        
        return features
    
    def rule_based_anomaly_detection(self, record_data: Dict) -> Dict[str, Any]:
        """Fallback rule-based anomaly detection"""
        anomalies = []
        score = 0.0
        
        # Age validation
        if 'age' in record_data:
            try:
                age = float(record_data['age'])
                if age < 0 or age > 120:
                    anomalies.append("Invalid age value")
                    score += 0.5
            except:
                anomalies.append("Non-numeric age value")
                score += 0.3
        
        # Amount validation
        amount_fields = ['face_amount', 'premium']
        for field in amount_fields:
            if field in record_data:
                try:
                    amount = float(record_data[field])
                    if amount <= 0:
                        anomalies.append(f"Invalid {field}: must be positive")
                        score += 0.3
                    elif amount > 50000000:  # $50M threshold
                        anomalies.append(f"Unusually high {field}")
                        score += 0.2
                except:
                    anomalies.append(f"Non-numeric {field}")
                    score += 0.3
        
        return {
            'is_anomaly': score > 0.5,
            'anomaly_score': min(1.0, score),
            'confidence': min(1.0, score),
            'method': 'rule_based',
            'details': anomalies
        }
    
    def learn_from_feedback(self, source_field: str, target_field: str, 
                          user_accepted: bool, confidence_score: float):
        """Learn from user feedback to improve future suggestions"""
        feedback_data = {
            'source_field': source_field,
            'target_field': target_field,
            'user_accepted': user_accepted,
            'confidence_score': confidence_score,
            'timestamp': datetime.now().isoformat()
        }
        
        # Store feedback for future model retraining
        try:
            with open('models/user_feedback.jsonl', 'a') as f:
                f.write(json.dumps(feedback_data) + '\n')
        except Exception as e:
            self.logger.error(f"Error storing user feedback: {e}")
    
    def retrain_models(self):
        """Retrain models based on accumulated user feedback"""
        # This would be implemented as a separate batch process
        # that runs periodically to improve model performance
        pass
```

### **Enhanced Excel Integration**

```python
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from typing import Dict, List, Any, Optional
import json

class EnhancedExcelManager:
    def __init__(self, ai_engine: Optional[AIEngine] = None):
        self.ai_engine = ai_engine
    
    def create_ai_enhanced_mapping_template(self, product_type: str, 
                                          sample_data: Optional[Dict] = None) -> str:
        """Create Excel template with AI-powered field suggestions"""
        
        # Define standard fields based on product type
        standard_fields = self.get_standard_fields(product_type)
        
        # If sample data provided, extract fields and get AI suggestions
        if sample_data and self.ai_engine:
            source_fields = list(sample_data.keys())
            mapping_data = []
            
            for source_field in source_fields:
                suggestions = self.ai_engine.get_field_suggestions(
                    source_field, standard_fields, product_type, top_k=3
                )
                
                # Use top suggestion as default, others as alternatives
                top_suggestion = suggestions[0] if suggestions else None
                
                row_data = {
                    'Source_Field': source_field,
                    'Target_Field': top_suggestion['target_field'] if top_suggestion else '',
                    'Values_Match': 'Auto-Suggested' if top_suggestion else 'Manual',
                    'Confidence_Score': top_suggestion['confidence'] if top_suggestion else 0.0,
                    'AI_Reasoning': top_suggestion['reasoning'] if top_suggestion else '',
                    'Alternative_1': suggestions[1]['target_field'] if len(suggestions) > 1 else '',
                    'Alternative_2': suggestions[2]['target_field'] if len(suggestions) > 2 else '',
                    'Sample_Value': str(sample_data.get(source_field, ''))[:50]  # Truncate for display
                }
                mapping_data.append(row_data)
        else:
            # Create basic template
            mapping_data = []
            for i in range(20):  # Create 20 empty rows
                mapping_data.append({
                    'Source_Field': '',
                    'Target_Field': '',
                    'Values_Match': '',
                    'Confidence_Score': '',
                    'AI_Reasoning': '',
                    'Alternative_1': '',
                    'Alternative_2': '',
                    'Sample_Value': ''
                })
        
        # Create Excel workbook
        wb = Workbook()
        
        # Main mapping sheet
        ws_mapping = wb.active
        ws_mapping.title = "Field_Mapping"
        
        # Headers
        headers = [
            'Source_Field', 'Target_Field', 'Values_Match', 'Confidence_Score',
            'AI_Reasoning', 'Alternative_1', 'Alternative_2', 'Sample_Value'
        ]
        
        # Add headers with styling
        for col, header in enumerate(headers, 1):
            cell = ws_mapping.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = Border(
                left=Side(style='thin'), right=Side(style='thin'),
                top=Side(style='thin'), bottom=Side(style='thin')
            )
        
        # Add data rows
        for row_idx, row_data in enumerate(mapping_data, 2):
            for col_idx, header in enumerate(headers, 1):
                value = row_data.get(header, '')
                cell = ws_mapping.cell(row=row_idx, column=col_idx, value=value)
                
                # Color code confidence scores
                if header == 'Confidence_Score' and value:
                    try:
                        confidence = float(value)
                        if confidence >= 0.8:
                            cell.fill = PatternFill(start_color="90EE90", end_color="90EE90", fill_type="solid")
                        elif confidence >= 0.6:
                            cell.fill = PatternFill(start_color="FFFF99", end_color="FFFF99", fill_type="solid")
                        else:
                            cell.fill = PatternFill(start_color="FFB6C1", end_color="FFB6C1", fill_type="solid")
                    except:
                        pass
        
        # Auto-adjust column widths
        for column in ws_mapping.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws_mapping.column_dimensions[column_letter].width = adjusted_width
        
        # Create standard fields reference sheet
        ws_reference = wb.create_sheet("Standard_Fields")
        ws_reference['A1'] = "Standard Fields Reference"
        ws_reference['A1'].font = Font(bold=True, size=14)
        
        for idx, field in enumerate(standard_fields, 3):
            ws_reference[f'A{idx}'] = field
        
        # Create instructions sheet
        ws_instructions = wb.create_sheet("Instructions")
        instructions = [
            "AI-Enhanced Field Mapping Template Instructions",
            "",
            "1. Source_Field: Enter the field name from your source data",
            "2. Target_Field: Select from standard fields or use AI suggestions",
            "3. Values_Match: Indicate if values match (Yes/No/Transform)",
            "4. Confidence_Score: AI confidence level (0.0 to 1.0)",
            "5. AI_Reasoning: Explanation for AI suggestion",
            "6. Alternative_1/2: Alternative field suggestions from AI",
            "7. Sample_Value: Sample data for verification",
            "",
            "Color Coding:",
            "• Green: High confidence (>= 0.8)",
            "• Yellow: Medium confidence (0.6 - 0.8)",
            "• Pink: Low confidence (< 0.6)",
            "",
            "Tips:",
            "• Review AI suggestions before accepting",
            "• Use alternatives if primary suggestion doesn't fit",
            "• Verify sample values match expected format",
            "• Save file before uploading to AIM system"
        ]
        
        for idx, instruction in enumerate(instructions, 1):
            cell = ws_instructions[f'A{idx}']
            cell.value = instruction
            if idx == 1:
                cell.font = Font(bold=True, size=14)
            elif instruction.startswith("•"):
                cell.font = Font(italic=True)
        
        # Save file
        filename = f"aim_mapping_template_{product_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        wb.save(filename)
        
        return filename
    
    def process_excel_upload_with_ai(self, filename: str, product_type: str) -> Dict[str, Any]:
        """Process uploaded Excel file with AI validation"""
        try:
            # Read Excel file
            df = pd.read_excel(filename, sheet_name='Field_Mapping')
            
            results = {
                'success': True,
                'processed_mappings': [],
                'validation_errors': [],
                'ai_suggestions': [],
                'statistics': {
                    'total_mappings': 0,
                    'valid_mappings': 0,
                    'ai_assisted': 0,
                    'manual_review_needed': 0
                }
            }
            
            for _, row in df.iterrows():
                if pd.isna(row['Source_Field']) or not str(row['Source_Field']).strip():
                    continue
                
                source_field = str(row['Source_Field']).strip()
                target_field = str(row['Target_Field']).strip() if not pd.isna(row['Target_Field']) else ''
                
                results['statistics']['total_mappings'] += 1
                
                # Validate mapping
                validation_result = self.validate_field_mapping(row, product_type)
                
                if validation_result['is_valid']:
                    results['processed_mappings'].append({
                        'source_field': source_field,
                        'target_field': target_field,
                        'confidence_score': validation_result.get('confidence_score', 0.0),
                        'validation_status': 'valid'
                    })
                    results['statistics']['valid_mappings'] += 1
                    
                    if validation_result.get('ai_assisted', False):
                        results['statistics']['ai_assisted'] += 1
                else:
                    results['validation_errors'].append({
                        'source_field': source_field,
                        'error': validation_result['error'],
                        'suggestion': validation_result.get('suggestion', '')
                    })
                    results['statistics']['manual_review_needed'] += 1
            
            return results
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error processing Excel file: {str(e)}",
                'processed_mappings': [],
                'validation_errors': [],
                'statistics': {}
            }
    
    def validate_field_mapping(self, row: pd.Series, product_type: str) -> Dict[str, Any]:
        """Validate individual field mapping with AI assistance"""
        source_field = str(row['Source_Field']).strip()
        target_field = str(row['Target_Field']).strip()
        
        # Basic validation
        if not source_field:
            return {'is_valid': False, 'error': 'Source field is required'}
        
        if not target_field:
            # Try to get AI suggestion
            if self.ai_engine:
                standard_fields = self.get_standard_fields(product_type)
                suggestions = self.ai_engine.get_field_suggestions(
                    source_field, standard_fields, product_type, top_k=1
                )
                
                if suggestions and suggestions[0]['confidence'] > 0.7:
                    return {
                        'is_valid': True,
                        'ai_assisted': True,
                        'confidence_score': suggestions[0]['confidence'],
                        'suggested_target': suggestions[0]['target_field']
                    }
            
            return {
                'is_valid': False, 
                'error': 'Target field is required',
                'suggestion': 'Use AI suggestions or select from standard fields'
            }
        
        # Validate target field is in standard fields
        standard_fields = self.get_standard_fields(product_type)
        if target_field not in standard_fields:
            return {
                'is_valid': False,
                'error': f'Target field "{target_field}" not in standard fields',
                'suggestion': f'Select from: {", ".join(standard_fields[:5])}...'
            }
        
        # Check confidence score if provided
        confidence_score = 0.0
        if not pd.isna(row.get('Confidence_Score')):
            try:
                confidence_score = float(row['Confidence_Score'])
                if confidence_score < 0 or confidence_score > 1:
                    return {
                        'is_valid': False,
                        'error': 'Confidence score must be between 0 and 1'
                    }
            except:
                confidence_score = 0.0
        
        return {
            'is_valid': True,
            'confidence_score': confidence_score,
            'ai_assisted': confidence_score > 0.5
        }
    
    def get_standard_fields(self, product_type: str) -> List[str]:
        """Get standard fields for product type"""
        standard_fields = {
            'life': [
                'policy_number', 'face_amount', 'premium', 'issue_date', 'effective_date',
                'insured_name', 'insured_age', 'insured_gender', 'smoking_status',
                'product_code', 'plan_code', 'death_benefit_option', 'premium_mode',
                'policy_status', 'cash_value', 'surrender_value', 'loan_amount',
                'dividend_option', 'beneficiary_name', 'owner_name', 'state_issued'
            ],
            'annuity': [
                'contract_number', 'account_value', 'premium_paid', 'issue_date',
                'effective_date', 'owner_name', 'owner_age', 'owner_gender',
                'product_code', 'contract_type', 'premium_mode', 'contract_status',
                'surrender_value', 'free_withdrawal_amount', 'death_benefit',
                'beneficiary_name', 'annuity_date', 'state_issued', 'market_value',
                'guaranteed_rate', 'current_rate', 'rider_codes'
            ]
        }
        
        return standard_fields.get(product_type, [])
```

---

## 📊 **Performance Monitoring and Optimization**

### **Performance Metrics Collection**

```python
import time
import psutil
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            'processing_times': [],
            'memory_usage': [],
            'cpu_usage': [],
            'operation_counts': {},
            'error_counts': {},
            'ai_performance': []
        }
        self.monitoring_active = False
        self.monitor_thread = None
    
    def start_monitoring(self):
        """Start background performance monitoring"""
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_system)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join()
    
    def _monitor_system(self):
        """Background system monitoring"""
        while self.monitoring_active:
            try:
                # Collect system metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory_info = psutil.virtual_memory()
                
                self.metrics['cpu_usage'].append({
                    'timestamp': datetime.now().isoformat(),
                    'cpu_percent': cpu_percent
                })
                
                self.metrics['memory_usage'].append({
                    'timestamp': datetime.now().isoformat(),
                    'memory_percent': memory_info.percent,
                    'memory_used_mb': memory_info.used / (1024 * 1024)
                })
                
                # Keep only last 1000 entries
                for key in ['cpu_usage', 'memory_usage']:
                    if len(self.metrics[key]) > 1000:
                        self.metrics[key] = self.metrics[key][-1000:]
                
                time.sleep(5)  # Monitor every 5 seconds
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(10)
    
    def record_operation_time(self, operation_name: str, execution_time: float):
        """Record operation execution time"""
        self.metrics['processing_times'].append({
            'operation': operation_name,
            'execution_time_ms': execution_time * 1000,
            'timestamp': datetime.now().isoformat()
        })
        
        # Update operation counts
        if operation_name not in self.metrics['operation_counts']:
            self.metrics['operation_counts'][operation_name] = 0
        self.metrics['operation_counts'][operation_name] += 1
    
    def record_ai_performance(self, operation: str, processing_time: float, 
                            accuracy: float, confidence: float):
        """Record AI-specific performance metrics"""
        self.metrics['ai_performance'].append({
            'operation': operation,
            'processing_time_ms': processing_time * 1000,
            'accuracy': accuracy,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        })
    
    def record_error(self, error_type: str, error_message: str):
        """Record error occurrences"""
        if error_type not in self.metrics['error_counts']:
            self.metrics['error_counts'][error_type] = 0
        self.metrics['error_counts'][error_type] += 1
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        now = datetime.now()
        one_hour_ago = now - timedelta(hours=1)
        
        # Calculate recent averages
        recent_processing_times = [
            entry for entry in self.metrics['processing_times']
            if datetime.fromisoformat(entry['timestamp']) > one_hour_ago
        ]
        
        recent_ai_performance = [
            entry for entry in self.metrics['ai_performance']
            if datetime.fromisoformat(entry['timestamp']) > one_hour_ago
        ]
        
        # Average processing times by operation
        operation_averages = {}
        for entry in recent_processing_times:
            op = entry['operation']
            if op not in operation_averages:
                operation_averages[op] = []
            operation_averages[op].append(entry['execution_time_ms'])
        
        for op in operation_averages:
            operation_averages[op] = sum(operation_averages[op]) / len(operation_averages[op])
        
        # AI performance averages
        ai_averages = {}
        for entry in recent_ai_performance:
            op = entry['operation']
            if op not in ai_averages:
                ai_averages[op] = {
                    'processing_times': [],
                    'accuracies': [],
                    'confidences': []
                }
            ai_averages[op]['processing_times'].append(entry['processing_time_ms'])
            ai_averages[op]['accuracies'].append(entry['accuracy'])
            ai_averages[op]['confidences'].append(entry['confidence'])
        
        for op in ai_averages:
            ai_averages[op] = {
                'avg_processing_time_ms': sum(ai_averages[op]['processing_times']) / len(ai_averages[op]['processing_times']),
                'avg_accuracy': sum(ai_averages[op]['accuracies']) / len(ai_averages[op]['accuracies']),
                'avg_confidence': sum(ai_averages[op]['confidences']) / len(ai_averages[op]['confidences'])
            }
        
        # System resource usage
        recent_cpu = [
            entry['cpu_percent'] for entry in self.metrics['cpu_usage']
            if datetime.fromisoformat(entry['timestamp']) > one_hour_ago
        ]
        
        recent_memory = [
            entry['memory_percent'] for entry in self.metrics['memory_usage']
            if datetime.fromisoformat(entry['timestamp']) > one_hour_ago
        ]
        
        return {
            'report_timestamp': now.isoformat(),
            'time_period': 'Last 1 hour',
            'operation_performance': operation_averages,
            'ai_performance': ai_averages,
            'system_resources': {
                'avg_cpu_percent': sum(recent_cpu) / len(recent_cpu) if recent_cpu else 0,
                'max_cpu_percent': max(recent_cpu) if recent_cpu else 0,
                'avg_memory_percent': sum(recent_memory) / len(recent_memory) if recent_memory else 0,
                'max_memory_percent': max(recent_memory) if recent_memory else 0
            },
            'operation_counts': self.metrics['operation_counts'],
            'error_counts': self.metrics['error_counts'],
            'total_operations': len(recent_processing_times),
            'total_ai_operations': len(recent_ai_performance)
        }

# Performance monitoring decorator
def monitor_performance(operation_name: str):
    """Decorator to monitor function performance"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Record successful operation
                if hasattr(wrapper, '_monitor'):
                    wrapper._monitor.record_operation_time(operation_name, execution_time)
                
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                
                # Record error
                if hasattr(wrapper, '_monitor'):
                    wrapper._monitor.record_error(operation_name, str(e))
                    wrapper._monitor.record_operation_time(f"{operation_name}_error", execution_time)
                
                raise
        
        return wrapper
    return decorator
```

This comprehensive technical implementation roadmap provides the foundation for building and deploying the AIM MVP with advanced AI capabilities, robust performance monitoring, and production-ready features. The modular architecture allows for incremental development and easy maintenance while ensuring scalability for future enhancements.
