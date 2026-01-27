import duckdb
import json
import os
import glob

def create_database():
    con = duckdb.connect('results.db')
    
    # Create the table
    con.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id VARCHAR,
            agent_id VARCHAR,
            agent_name VARCHAR,
            timestamp VARCHAR,
            execution_correctness FLOAT,
            style_score FLOAT,
            conciseness FLOAT,
            relevance FLOAT,
            overall_score FLOAT,
            reasoning VARCHAR
        )
    """)
    
    # Clear existing data to avoid duplicates if re-running (simplest approach for now)
    con.execute("DELETE FROM results")
    
    # Load all JSON files from results/ directory
    json_files = glob.glob("results/*.json")
    print(f"Found {len(json_files)} result files.")
    
    for file_path in json_files:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            # Extract fields
            record_id = data.get('id')
            agent_id = data.get('agent_id')
            agent_name = data.get('agent_name')
            timestamp = data.get('timestamp')
            
            # Support both flat and nested structures
            if 'evaluation' in data:
                evaluation = data.get('evaluation', {})
                exe = evaluation.get('execution_correctness')
                style = evaluation.get('style_score')
                concise = evaluation.get('conciseness')
                rel = evaluation.get('relevance')
                overall = evaluation.get('overall_score')
                reasoning = evaluation.get('reasoning')
            else:
                # Flat structure (scores at top level)
                exe = data.get('execution_correctness')
                style = data.get('style_score')
                concise = data.get('conciseness')
                rel = data.get('relevance')
                overall = data.get('overall_score')
                reasoning = data.get('reasoning')
            
            con.execute("""
                INSERT INTO results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (record_id, agent_id, agent_name, timestamp, exe, style, concise, rel, overall, reasoning))
            
            print(f"Imported {file_path}")
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    # Verify count
    count = con.execute("SELECT COUNT(*) FROM results").fetchone()[0]
    print(f"Total records in DuckDB: {count}")
    
    con.close()

if __name__ == "__main__":
    create_database()
