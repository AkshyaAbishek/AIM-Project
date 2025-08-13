# AI-Enhanced AIM Processor - Implementation Example
# This file demonstrates how AI toolkits will be integrated into the existing AIM project

"""
Enhanced AIM Processor with AI Capabilities

This implementation shows how AI toolkits are integrated into the existing
AIM (Actuarial Input Mapper) system to provide intelligent data processing,
validation, and analysis capabilities.
"""

import json
import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

# AI Toolkit Imports
from sklearn.ensemble import IsolationForest
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import spacy
from transformers import (
    AutoTokenizer, AutoModel, 
    pipeline, T5Tokenizer, T5ForConditionalGeneration
)
import openai
import xgboost as xgb

# Existing AIM imports
from src.aim_processor import AIMProcessor
from common.database_manager import DatabaseManager
from common.ui_utils import UIUtils


class AIEnhancedAIMProcessor:
    """
    AI-Enhanced version of the AIM Processor that integrates multiple AI toolkits
    for intelligent actuarial data processing.
    
    This class demonstrates the practical application of AI toolkits including:
    - Machine Learning for field mapping and validation
    - NLP for document processing and text analysis
    - Anomaly detection for data quality assurance
    - Predictive modeling for risk assessment
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the AI-Enhanced AIM Processor with all AI components."""
        
        # Initialize base AIM processor
        self.base_processor = AIMProcessor(config_path)
        
        # Initialize AI components
        self.smart_mapper = SmartFieldMapper()
        self.document_processor = DocumentIntelligenceEngine()
        self.validator = AIValidationEngine()
        self.risk_assessor = RiskAssessmentAI()
        self.nlp_generator = NaturalLanguageGenerator()
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("AI-Enhanced AIM Processor initialized with all AI toolkits")
    
    def process_with_ai_enhancement(self, input_data: Dict[str, Any], 
                                  product_type: str = "life") -> Dict[str, Any]:
        """
        Process actuarial data with full AI enhancement pipeline.
        
        Use Case 1: Intelligent Field Mapping
        Use Case 2: AI-Powered Validation  
        Use Case 3: Risk Assessment
        Use Case 4: Natural Language Reporting
        """
        
        self.logger.info(f"Starting AI-enhanced processing for {product_type}")
        
        # Step 1: Smart Field Mapping with AI
        mapped_data = self.smart_mapper.auto_map_fields(input_data, product_type)
        
        # Step 2: AI-Powered Data Validation
        validation_result = self.validator.comprehensive_validation(mapped_data)
        
        # Step 3: Risk Assessment with Machine Learning
        risk_analysis = self.risk_assessor.assess_application_risk(mapped_data)
        
        # Step 4: Process with base AIM processor
        base_result = self.base_processor.process_fast_ui_input(
            mapped_data, product_type, "full"
        )
        
        # Step 5: Generate AI-Enhanced Report
        ai_report = self.nlp_generator.create_comprehensive_report(
            base_result, validation_result, risk_analysis
        )
        
        # Combine all results
        enhanced_result = {
            **base_result,
            "ai_enhancements": {
                "smart_mapping": {
                    "confidence_score": mapped_data.get("_mapping_confidence", 0),
                    "auto_mapped_fields": mapped_data.get("_auto_mapped", []),
                    "suggestions": mapped_data.get("_suggestions", [])
                },
                "validation": validation_result,
                "risk_assessment": risk_analysis,
                "ai_report": ai_report,
                "processing_metadata": {
                    "ai_toolkit_version": "1.0.0",
                    "models_used": self.get_models_used(),
                    "confidence_scores": self.calculate_overall_confidence(
                        validation_result, risk_analysis
                    )
                }
            }
        }
        
        self.logger.info("AI-enhanced processing completed successfully")
        return enhanced_result


class SmartFieldMapper:
    """
    AI-powered field mapping using semantic similarity and machine learning.
    
    Demonstrates Use Case 1: Intelligent Field Mapping with AI Toolkits
    - Uses transformers for semantic understanding
    - Implements similarity-based field matching
    - Provides confidence scores and suggestions
    """
    
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
        self.model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
        self.field_embeddings_cache = {}
        
        # Standard actuarial field mappings (learned from training data)
        self.standard_fields = {
            "life": [
                "insured_first_name", "insured_last_name", "insured_birth_date",
                "insured_gender", "coverage_amount", "premium_mode",
                "beneficiary_name", "policy_effective_date"
            ],
            "annuity": [
                "annuitant_first_name", "annuitant_last_name", "annuitant_birth_date",
                "annuitant_gender", "premium_amount", "payout_start_date"
            ]
        }
    
    def auto_map_fields(self, input_data: Dict[str, Any], 
                       product_type: str) -> Dict[str, Any]:
        """
        Automatically map input fields to standard actuarial fields using AI.
        
        This demonstrates how AI toolkits solve the manual field mapping problem:
        - Semantic similarity using transformer models
        - Confidence scoring for mapping quality
        - Automatic suggestions for unclear mappings
        """
        
        mapped_data = {}
        mapping_metadata = {
            "_mapping_confidence": 0,
            "_auto_mapped": [],
            "_suggestions": [],
            "_manual_review_needed": []
        }
        
        target_fields = self.standard_fields.get(product_type, [])
        total_confidence = 0
        
        for input_field, value in input_data.items():
            if input_field.startswith("_"):  # Skip metadata fields
                continue
                
            # Find best matching target field using AI
            best_match, confidence = self.find_semantic_match(input_field, target_fields)
            
            if confidence > 0.8:  # High confidence mapping
                mapped_data[best_match] = value
                mapping_metadata["_auto_mapped"].append({
                    "source": input_field,
                    "target": best_match,
                    "confidence": confidence
                })
            elif confidence > 0.5:  # Medium confidence - suggest for review
                mapped_data[best_match] = value
                mapping_metadata["_suggestions"].append({
                    "source": input_field,
                    "suggested_target": best_match,
                    "confidence": confidence,
                    "alternatives": self.get_alternative_matches(input_field, target_fields)
                })
            else:  # Low confidence - needs manual review
                mapped_data[input_field] = value  # Keep original field name
                mapping_metadata["_manual_review_needed"].append({
                    "field": input_field,
                    "value": value,
                    "reason": "Low confidence in automatic mapping"
                })
            
            total_confidence += confidence
        
        # Calculate overall mapping confidence
        if len(input_data) > 0:
            mapping_metadata["_mapping_confidence"] = total_confidence / len(input_data)
        
        # Add metadata to mapped data
        mapped_data.update(mapping_metadata)
        
        return mapped_data
    
    def find_semantic_match(self, source_field: str, 
                           target_fields: List[str]) -> Tuple[str, float]:
        """Use transformer models to find semantic similarity between fields."""
        
        source_embedding = self.get_field_embedding(source_field)
        target_embeddings = [self.get_field_embedding(field) for field in target_fields]
        
        similarities = cosine_similarity([source_embedding], target_embeddings)[0]
        best_match_idx = np.argmax(similarities)
        confidence = similarities[best_match_idx]
        
        return target_fields[best_match_idx], float(confidence)
    
    def get_field_embedding(self, field_name: str) -> np.ndarray:
        """Get semantic embedding for a field name using transformer model."""
        
        if field_name in self.field_embeddings_cache:
            return self.field_embeddings_cache[field_name]
        
        # Preprocess field name for better semantic understanding
        processed_name = field_name.replace("_", " ").replace("-", " ").lower()
        
        inputs = self.tokenizer(processed_name, return_tensors="pt", 
                               padding=True, truncation=True)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        
        self.field_embeddings_cache[field_name] = embedding
        return embedding


class DocumentIntelligenceEngine:
    """
    NLP-powered document processing for extracting structured data from text.
    
    Demonstrates Use Case 2: Natural Language Data Extraction
    - Uses spaCy for entity recognition
    - Implements transformers for text understanding
    - Extracts structured data from unstructured text
    """
    
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.ner_pipeline = pipeline("ner", 
                                   model="dbmdz/bert-large-cased-finetuned-conll03-english")
        self.qa_pipeline = pipeline("question-answering")
    
    def process_document(self, document_text: str) -> Dict[str, Any]:
        """
        Extract structured data from unstructured insurance documents.
        
        Real-world use cases:
        - Process scanned insurance applications
        - Extract data from email communications  
        - Parse PDF forms and convert to structured format
        """
        
        # Named Entity Recognition
        doc = self.nlp(document_text)
        entities = self.ner_pipeline(document_text)
        
        # Extract specific insurance-related information
        extracted_data = {
            "applicant_info": self.extract_applicant_information(document_text),
            "policy_details": self.extract_policy_details(document_text),
            "financial_info": self.extract_financial_information(document_text),
            "dates": self.extract_important_dates(doc),
            "entities": self.process_named_entities(entities),
            "confidence_score": self.calculate_extraction_confidence(doc, entities)
        }
        
        return extracted_data
    
    def extract_applicant_information(self, text: str) -> Dict[str, Any]:
        """Extract applicant information using question-answering models."""
        
        questions = [
            "What is the applicant's first name?",
            "What is the applicant's last name?", 
            "What is the applicant's date of birth?",
            "What is the applicant's gender?",
            "What is the applicant's address?"
        ]
        
        applicant_info = {}
        for question in questions:
            try:
                answer = self.qa_pipeline(question=question, context=text)
                field_name = self.question_to_field_name(question)
                applicant_info[field_name] = {
                    "value": answer["answer"],
                    "confidence": answer["score"]
                }
            except Exception as e:
                self.logger.warning(f"Could not extract answer for: {question}")
        
        return applicant_info


class AIValidationEngine:
    """
    Machine learning-powered data validation and anomaly detection.
    
    Demonstrates Use Case 3: Predictive Data Validation
    - Uses scikit-learn for anomaly detection
    - Implements validation rules with ML models
    - Provides confidence scores and risk flags
    """
    
    def __init__(self):
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.validation_rules = self.load_validation_rules()
        
        # Train models with historical data (in production, this would be pre-trained)
        self.train_validation_models()
    
    def comprehensive_validation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive AI-powered validation on actuarial data.
        
        Business value:
        - Detect anomalies in real-time
        - Flag suspicious data patterns
        - Provide confidence scores for data quality
        - Suggest corrections for invalid data
        """
        
        validation_result = {
            "is_valid": True,
            "overall_confidence": 0.0,
            "anomaly_detection": {},
            "field_validation": {},
            "risk_flags": [],
            "suggestions": []
        }
        
        # Extract numerical features for anomaly detection
        numerical_features = self.extract_numerical_features(data)
        
        if numerical_features:
            # Anomaly detection using Isolation Forest
            scaled_features = self.scaler.transform([numerical_features])
            anomaly_score = self.anomaly_detector.decision_function(scaled_features)[0]
            is_anomaly = self.anomaly_detector.predict(scaled_features)[0] == -1
            
            validation_result["anomaly_detection"] = {
                "is_anomaly": bool(is_anomaly),
                "anomaly_score": float(anomaly_score),
                "confidence": abs(float(anomaly_score))
            }
        
        # Field-level validation with ML
        for field, value in data.items():
            if not field.startswith("_"):
                field_validation = self.validate_field_with_ai(field, value, data)
                validation_result["field_validation"][field] = field_validation
                
                if not field_validation["is_valid"]:
                    validation_result["is_valid"] = False
        
        # Calculate overall confidence
        confidence_scores = [
            validation_result["anomaly_detection"].get("confidence", 0),
            *[fv.get("confidence", 0) for fv in validation_result["field_validation"].values()]
        ]
        validation_result["overall_confidence"] = np.mean(confidence_scores)
        
        # Generate risk flags and suggestions
        validation_result["risk_flags"] = self.generate_risk_flags(data, validation_result)
        validation_result["suggestions"] = self.generate_improvement_suggestions(data, validation_result)
        
        return validation_result


class RiskAssessmentAI:
    """
    Machine learning-powered risk assessment for insurance applications.
    
    Demonstrates Use Case 4: Intelligent Risk Assessment and Pricing
    - Uses XGBoost for risk prediction
    - Implements feature engineering for actuarial factors
    - Provides risk scores and pricing recommendations
    """
    
    def __init__(self):
        self.risk_model = xgb.XGBClassifier(random_state=42)
        self.pricing_model = xgb.XGBRegressor(random_state=42)
        self.feature_names = []
        
        # In production, these would be pre-trained models
        self.train_risk_models()
    
    def assess_application_risk(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-powered risk assessment for insurance applications.
        
        Business applications:
        - Automated underwriting decisions
        - Dynamic pricing based on risk factors
        - Fraud detection and prevention
        - Portfolio risk management
        """
        
        # Extract and engineer features for risk assessment
        risk_features = self.engineer_risk_features(application_data)
        
        if not risk_features:
            return {"error": "Insufficient data for risk assessment"}
        
        # Risk classification
        risk_probability = self.risk_model.predict_proba([risk_features])[0]
        risk_score = risk_probability[1]  # Probability of high risk
        
        # Risk category classification
        risk_category = self.classify_risk_level(risk_score)
        
        # Pricing recommendation
        suggested_premium = self.pricing_model.predict([risk_features])[0]
        
        # Feature importance for explainability
        feature_importance = self.get_feature_importance(risk_features)
        
        risk_assessment = {
            "risk_score": float(risk_score),
            "risk_category": risk_category,
            "suggested_premium": float(suggested_premium),
            "confidence": float(max(risk_probability)),
            "key_risk_factors": feature_importance[:5],  # Top 5 factors
            "recommendations": self.generate_risk_recommendations(risk_category, risk_score),
            "underwriting_decision": self.make_underwriting_recommendation(risk_score),
            "pricing_factors": self.explain_pricing_factors(risk_features)
        }
        
        return risk_assessment


class NaturalLanguageGenerator:
    """
    AI-powered natural language report generation.
    
    Demonstrates Use Case 6: Automated Report Generation
    - Uses T5 for text summarization and generation
    - Creates natural language explanations
    - Generates comprehensive actuarial reports
    """
    
    def __init__(self):
        self.tokenizer = T5Tokenizer.from_pretrained("t5-base")
        self.model = T5ForConditionalGeneration.from_pretrained("t5-base")
    
    def create_comprehensive_report(self, processing_result: Dict[str, Any],
                                  validation_result: Dict[str, Any],
                                  risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive natural language reports for actuarial analysis.
        
        Business value:
        - Automated report generation saves hours of manual work
        - Consistent, professional reporting format
        - Natural language explanations for technical results
        - Actionable insights and recommendations
        """
        
        # Create executive summary
        executive_summary = self.generate_executive_summary(
            processing_result, validation_result, risk_assessment
        )
        
        # Generate detailed analysis
        detailed_analysis = self.create_detailed_analysis(
            processing_result, validation_result, risk_assessment
        )
        
        # Create recommendations
        recommendations = self.generate_actionable_recommendations(
            validation_result, risk_assessment
        )
        
        ai_report = {
            "executive_summary": executive_summary,
            "detailed_analysis": detailed_analysis,
            "risk_assessment_summary": self.summarize_risk_assessment(risk_assessment),
            "data_quality_report": self.summarize_data_quality(validation_result),
            "recommendations": recommendations,
            "next_steps": self.generate_next_steps(risk_assessment),
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "report_type": "AI_Enhanced_Actuarial_Analysis",
                "confidence_level": self.calculate_report_confidence(
                    validation_result, risk_assessment
                )
            }
        }
        
        return ai_report


# Example usage demonstrating AI toolkit integration
def demonstrate_ai_enhanced_processing():
    """
    Demonstration of how AI toolkits enhance the existing AIM system.
    
    This example shows the practical integration of multiple AI technologies
    into a real-world actuarial data processing workflow.
    """
    
    print("🤖 AI-Enhanced AIM Processor Demonstration")
    print("=" * 60)
    
    # Sample input data (could come from various sources)
    sample_input = {
        "applicant_first_name": "John",
        "applicant_last_name": "Doe", 
        "applicant_birth_date": "1985-06-15",
        "applicant_gender": "M",
        "policy_face_amount": "250000",
        "policy_effective_date": "2024-01-01",
        "premium_mode": "M",
        "applicant_income": "75000",
        "applicant_occupation": "Software Engineer"
    }
    
    # Initialize AI-enhanced processor
    ai_processor = AIEnhancedAIMProcessor()
    
    # Process with full AI enhancement
    result = ai_processor.process_with_ai_enhancement(sample_input, "life")
    
    # Display results
    print("\n📊 Processing Results:")
    print(f"✅ Status: {result['status']}")
    print(f"🎯 AI Mapping Confidence: {result['ai_enhancements']['smart_mapping']['confidence_score']:.2f}")
    print(f"🛡️ Data Validation: {'PASSED' if result['ai_enhancements']['validation']['is_valid'] else 'FAILED'}")
    print(f"⚠️ Risk Score: {result['ai_enhancements']['risk_assessment']['risk_score']:.2f}")
    print(f"💰 Suggested Premium: ${result['ai_enhancements']['risk_assessment']['suggested_premium']:.2f}")
    
    print("\n📝 AI-Generated Executive Summary:")
    print(result['ai_enhancements']['ai_report']['executive_summary'])
    
    print("\n🔍 Key Risk Factors:")
    for factor in result['ai_enhancements']['risk_assessment']['key_risk_factors']:
        print(f"  • {factor}")
    
    print("\n💡 Recommendations:")
    for rec in result['ai_enhancements']['ai_report']['recommendations']:
        print(f"  • {rec}")


if __name__ == "__main__":
    # Run the demonstration
    demonstrate_ai_enhanced_processing()
    
    print("\n🎉 AI Toolkit Integration Complete!")
    print("This demonstrates how modern AI technologies can enhance")
    print("traditional actuarial data processing workflows.")
