"""
Secure Smart Contract Environment

Implements a sandboxed environment for executing untrusted smart contract
code safely within the SeirChain Virtual Machine.
"""

import ast
import builtins
import sys
from typing import Dict, Any, List, Optional
import threading


class SecureExecutionEnvironment:
    """
    Provides a sandboxed environment for executing smart contracts safely.
    """
    
    def __init__(self):
        """Initialize the secure execution environment."""
        self.allowed_builtins = {
            'len', 'range', 'enumerate', 'zip', 'map', 'filter',
            'sum', 'min', 'max', 'abs', 'round', 'int', 'float', 'str',
            'bool', 'list', 'dict', 'set', 'tuple'
        }
        
        self.blocked_modules = {
            'os', 'sys', 'subprocess', 'socket', 'urllib', 'requests',
            'http', 'ftplib', 'smtplib', 'sqlite3', 'pickle', 'marshal'
        }
        
        self.execution_context = threading.local()
        
    def create_safe_globals(self, custom_globals: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create a safe global namespace for contract execution.
        
        Args:
            custom_globals: Additional globals to include
            
        Returns:
            Safe global namespace dictionary
        """
        safe_globals = {
            '__builtins__': {
                name: getattr(builtins, name) 
                for name in self.allowed_builtins 
                if hasattr(builtins, name)
            }
        }
        
        if custom_globals:
            safe_globals.update(custom_globals)
            
        return safe_globals
    
    def validate_ast(self, code: str) -> bool:
        """
        Validate the AST of the contract code for safety.
        
        Args:
            code: Python code to validate
            
        Returns:
            True if code is safe, False otherwise
        """
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                # Block import statements
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.ImportFrom):
                        if node.module in self.blocked_modules:
                            return False
                    return False
                
                # Block exec and eval
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in ['exec', 'eval', '__import__']:
                            return False
                
                # Block attribute access to dangerous modules
                if isinstance(node, ast.Attribute):
                    if isinstance(node.value, ast.Name):
                        if node.value.id in self.blocked_modules:
                            return False
            
            return True
            
        except SyntaxError:
            return False
    
    def execute_contract(self, code: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute smart contract code in a secure environment.
        
        Args:
            code: Python code to execute
            context: Execution context variables
            
        Returns:
            Dictionary with execution results
        """
        if not self.validate_ast(code):
            return {'error': 'Invalid or unsafe code', 'success': False}
        
        safe_globals = self.create_safe_globals(context or {})
        safe_locals = {}
        
        try:
            # Compile and execute in restricted environment
            compiled_code = compile(code, '<smart_contract>', 'exec')
            exec(compiled_code, safe_globals, safe_locals)
            
            return {
                'success': True,
                'result': safe_locals,
                'globals': safe_globals
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'type': type(e).__name__
            }
    
    def execute_function(self, code: str, function_name: str, 
                        args: List[Any] = None, kwargs: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute a specific function from smart contract code.
        
        Args:
            code: Python code containing the function
            function_name: Name of the function to execute
            args: Positional arguments
            kwargs: Keyword arguments
            
        Returns:
            Dictionary with execution results
        """
        if not self.validate_ast(code):
            return {'error': 'Invalid or unsafe code', 'success': False}
        
        safe_globals = self.create_safe_globals()
        safe_locals = {}
        
        try:
            # Execute the code to define functions
            compiled_code = compile(code, '<smart_contract>', 'exec')
            exec(compiled_code, safe_globals, safe_locals)
            
            # Check if function exists
            if function_name not in safe_locals:
                return {'error': f'Function {function_name} not found', 'success': False}
            
            func = safe_locals[function_name]
            if not callable(func):
                return {'error': f'{function_name} is not callable', 'success': False}
            
            # Execute the function
            args = args or []
            kwargs = kwargs or {}
            result = func(*args, **kwargs)
            
            return {
                'success': True,
                'result': result
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'type': type(e).__name__
            }


class DeterministicExecution:
    """
    Ensures deterministic execution of smart contracts.
    """
    
    @staticmethod
    def make_deterministic(code: str) -> str:
        """
        Transform code to ensure deterministic execution.
        
        Args:
            code: Original Python code
            
        Returns:
            Modified code with deterministic behavior
        """
        # Remove non-deterministic imports and functions
        lines = code.split('\n')
        deterministic_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Remove random module usage
            if 'import random' in line or 'from random' in line:
                continue
            
            # Remove time module usage
            if 'import time' in line or 'from time' in line:
                continue
            
            # Remove datetime usage
            if 'import datetime' in line or 'from datetime' in line:
                continue
            
            # Remove direct usage of non-deterministic functions
            if 'random.' in line or 'time.' in line or 'datetime.' in line:
                continue
                
            deterministic_lines.append(line)
        
        return '\n'.join(deterministic_lines)
    
    @staticmethod
    def validate_deterministic(code: str) -> bool:
        """
        Check if code is deterministic.
        
        Args:
            code: Python code to check
            
        Returns:
            True if code is deterministic, False otherwise
        """
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                # Check for random module usage
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name == 'random':
                            return False
                
                if isinstance(node, ast.ImportFrom):
                    if node.module == 'random':
                        return False
                
                # Check for time module usage
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in ['time', 'datetime']:
                            return False
                
                if isinstance(node, ast.ImportFrom):
                    if node.module in ['time', 'datetime']:
                        return False
            
            return True
            
        except SyntaxError:
            return False


# Example usage
if __name__ == "__main__":
    # Test secure execution
    env = SecureExecutionEnvironment()
    
    # Safe contract
    safe_code = """
def add(a, b):
    return a + b

result = add(5, 3)
"""
    
    result = env.execute_contract(safe_code)
    print("Safe contract result:", result)
    
    # Unsafe contract
    unsafe_code = """
import os
os.system('rm -rf /')
"""
    
    result = env.execute_contract(unsafe_code)
    print("Unsafe contract result:", result)
    
    # Test deterministic execution
    det = DeterministicExecution()
    print("Is deterministic:", det.validate_deterministic(safe_code))
