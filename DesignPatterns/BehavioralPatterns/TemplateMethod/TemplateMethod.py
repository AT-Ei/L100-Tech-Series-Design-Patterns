from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json
import csv

# Abstract Class
class DataProcessor(ABC):
    """Abstract base class for data processors with template method"""
    
    def process_data(self, input_file: str, output_file: str) -> None:
        """Template method defining the data processing algorithm"""
        print(f"\n=== Processing {input_file} ===")
        
        # Step 1: Read data from file
        data = self._read_data(input_file)
        print(f"Read {len(data)} records from {input_file}")
        
        # Step 2: Validate data (optional step)
        if self._should_validate():
            data = self._validate_data(data)
            print("Data validation completed")
        
        # Step 3: Transform data (implemented by subclasses)
        transformed_data = self._transform_data(data)
        print("Data transformation completed")
        
        # Step 4: Save processed data
        self._save_data(transformed_data, output_file)
        print(f"Saved processed data to {output_file}")
    
    def _read_data(self, filename: str) -> List[Dict[str, Any]]:
        """Read data from file (common implementation)"""
        print(f"Reading data from {filename}...")
        # In a real implementation, this would read from the file
        # For demonstration, we'll use sample data
        if filename.endswith('.csv'):
            return self._read_csv(filename)
        elif filename.endswith('.json'):
            return self._read_json(filename)
        else:
            raise ValueError("Unsupported file format")
    
    def _read_csv(self, filename: str) -> List[Dict[str, Any]]:
        """Read CSV data (simulated)"""
        print("Using CSV reader")
        # Simulated CSV data
        return [
            {"id": 1, "name": "Alice", "age": 30, "salary": 50000},
            {"id": 2, "name": "Bob", "age": 25, "salary": 45000},
            {"id": 3, "name": "Charlie", "age": 35, "salary": 60000}
        ]
    
    def _read_json(self, filename: str) -> List[Dict[str, Any]]:
        """Read JSON data (simulated)"""
        print("Using JSON reader")
        # Simulated JSON data
        return [
            {"id": 1, "name": "Alice", "age": 30, "salary": 50000},
            {"id": 2, "name": "Bob", "age": 25, "salary": 45000},
            {"id": 3, "name": "Charlie", "age": 35, "salary": 60000}
        ]
    
    def _should_validate(self) -> bool:
        """Hook method to determine if validation is needed"""
        return True
    
    def _validate_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate data (can be overridden by subclasses)"""
        print("Validating data...")
        # Remove records with missing required fields
        validated_data = []
        for record in data:
            if all(key in record for key in ["id", "name", "age", "salary"]):
                validated_data.append(record)
            else:
                print(f"Skipping invalid record: {record}")
        return validated_data
    
    @abstractmethod
    def _transform_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform data (must be implemented by subclasses)"""
        pass
    
    def _save_data(self, data: List[Dict[str, Any]], filename: str) -> None:
        """Save data to file (common implementation)"""
        print(f"Saving data to {filename}...")
        # In a real implementation, this would write to the file
        # For demonstration, we'll just print the data
        print("Sample of saved data:")
        for i, record in enumerate(data[:2]):  # Show first 2 records
            print(f"  {i+1}. {record}")
        if len(data) > 2:
            print(f"  ... and {len(data) - 2} more records")

# Concrete Classes
class CSVDataProcessor(DataProcessor):
    """Processor for CSV data"""
    
    def _transform_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform CSV data by adding a calculated field"""
        print("Transforming CSV data...")
        transformed_data = []
        for record in data:
            # Add a calculated field: salary per year of age
            record["salary_per_age"] = record["salary"] / record["age"]
            # Round salary to nearest thousand
            record["salary"] = round(record["salary"], -3)
            transformed_data.append(record)
        return transformed_data
    
    def _should_validate(self) -> bool:
        """Override to skip validation for CSV"""
        return False

class JSONDataProcessor(DataProcessor):
    """Processor for JSON data"""
    
    def _transform_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform JSON data by filtering and restructuring"""
        print("Transforming JSON data...")
        transformed_data = []
        for record in data:
            # Only include records with salary >= 50000
            if record["salary"] >= 50000:
                # Restructure the record
                transformed_record = {
                    "employee_id": record["id"],
                    "full_name": record["name"],
                    "details": {
                        "age": record["age"],
                        "annual_salary": record["salary"]
                    }
                }
                transformed_data.append(transformed_record)
        return transformed_data
    
    def _validate_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Override to add additional validation for JSON"""
        print("Validating JSON data with additional checks...")
        validated_data = super()._validate_data(data)
        # Additional validation: ensure age is reasonable
        return [record for record in validated_data if 18 <= record["age"] <= 65]

# Client
def main():
    # Create processors
    csv_processor = CSVDataProcessor()
    json_processor = JSONDataProcessor()
    
    # Process CSV data
    print("=== CSV Data Processing ===")
    csv_processor.process_data("input.csv", "output.csv")
    
    # Process JSON data
    print("\n=== JSON Data Processing ===")
    json_processor.process_data("input.json", "output.json")
    
    # Demonstrate the template method structure
    print("\n=== Template Method Structure ===")
    print("The template method 'process_data' defines the algorithm:")
    print("1. _read_data() - Common implementation")
    print("2. _should_validate() - Hook method (can be overridden)")
    print("3. _validate_data() - Common implementation (can be overridden)")
    print("4. _transform_data() - Abstract method (must be implemented)")
    print("5. _save_data() - Common implementation")
    print("\nSubclasses can override specific steps without changing the structure.")

if __name__ == "__main__":
    main()