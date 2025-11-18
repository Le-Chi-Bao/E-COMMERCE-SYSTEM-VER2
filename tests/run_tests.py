import unittest
import sys
import os

def run_all_tests():
    """Chạy toàn bộ test cases"""
    # Thêm thư mục gốc vào path
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    
    # Tìm và chạy tất cả tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Chạy tests với output chi tiết
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # In kết quả tổng quan
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {(result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100:.1f}%")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)