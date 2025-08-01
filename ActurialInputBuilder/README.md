# Actuarial Input Builder

## Problem Statement

In current actuarial calculation validation, we map the inputs manually from FAST UI to product-specific actuarial calculations that contain all business logic. This manual process:

- **Takes significant time** for each validation
- **Prone to manual errors** during input mapping
- **Lacks standardization** across different products
- **Difficult to maintain** when business logic changes

## Solution Overview

The Actuarial Input Builder automates the mapping process between FAST UI inputs and product-specific actuarial calculation engines, reducing time and eliminating manual errors.

## Project Structure

```
ActurialInputBuilder/
├── src/
│   ├── mappers/           # Input mapping logic
│   ├── validators/        # Input validation rules
│   ├── calculators/       # Actuarial calculation engines
│   ├── parsers/          # FAST UI data parsers
│   └── config/           # Configuration and mapping rules
├── data/
│   ├── schemas/          # Input/output schemas
│   ├── templates/        # Mapping templates
│   └── sample/           # Sample data files
├── tests/
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── docs/                # Documentation
└── scripts/             # Utility scripts
```

## Features

### 🔄 **Automated Input Mapping**
- Seamless conversion from FAST UI format to actuarial calc format
- Support for multiple product types
- Configurable mapping rules

### ✅ **Input Validation**
- Comprehensive validation of all input parameters
- Business rule enforcement
- Error detection and reporting

### 🎯 **Product-Specific Logic**
- Modular design for different insurance products
- Extensible framework for new products
- Centralized business logic management

### 📊 **Monitoring & Logging**
- Detailed audit trails
- Performance monitoring
- Error tracking and reporting

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Product Mappings**:
   - Edit `src/config/product_mappings.json`
   - Define your FAST UI to actuarial calc mappings

3. **Run Input Builder**:
   ```python
   from src.input_builder import ActurialInputBuilder
   
   builder = ActurialInputBuilder()
   result = builder.process_fast_ui_input(input_data, product_type)
   ```

## Configuration

The system uses JSON-based configuration files to define:
- Field mappings between FAST UI and actuarial calculations
- Validation rules and business logic
- Product-specific transformations
- Error handling strategies

## Benefits

- ⏱️ **Time Savings**: Reduce manual mapping time by 80-90%
- 🎯 **Accuracy**: Eliminate manual mapping errors
- 🔧 **Maintainability**: Centralized mapping configuration
- 📈 **Scalability**: Easy addition of new products and rules
- 🔍 **Auditability**: Complete traceability of input transformations

## License

Internal use only - Actuarial Systems Team
