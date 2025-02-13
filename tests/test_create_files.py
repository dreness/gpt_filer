import os
import shutil
import json
import unittest
import uuid
from server.create_files import create_files_from_json

class TestCreateFiles(unittest.TestCase):
    def setUp(self):
        # stash current directory
        self.cwd = os.getcwd()
        # create a temporary directory inside the test directory with a pseudo-random name
        dir_name = str(uuid.uuid4())
        print(dir_name)
        self.test_dir = os.path.join("tests", dir_name)
        os.mkdir(self.test_dir)
        print(self.test_dir)
        self.test_json = os.path.join(self.test_dir, "test_code_files.json")

        # Create a sample JSON file
        data = [
            {
                "id": 1,
                "path": os.path.join(self.test_dir, "test1.py"),
                "code": "# test1"
            },
            {
                "id": 2,
                "path": os.path.join(self.test_dir, "subdir/sub2/test2.py"),
                "code": "# test2"
            }
        ]
        with open(self.test_json, 'w', encoding='utf-8') as f:
            json.dump(data, f)

    def tearDown(self):
        # Clean up the directory created in setUp, even if it still contains files
        print(f"Cleaning up {self.test_dir}")
        # print current directory
        print(os.getcwd())
        # remove all files from self.test_dir
        #os.chdir(self.test_dir)
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        shutil.rmtree(self.test_dir)
        #os.rmdir(self.test_dir)
        
        # return to the original directory
        os.chdir(self.cwd) 


    def test_file_creation(self):
        create_files_from_json(self.test_json)

        file1_path = os.path.join(self.test_dir, "test1.py")
        file2_path = os.path.join(self.test_dir, "subdir/sub2/test2.py")

        self.assertTrue(os.path.exists(file1_path))
        self.assertTrue(os.path.exists(file2_path))

        with open(file1_path, 'r') as f1:
            self.assertEqual(f1.read(), "# test1")

        with open(file2_path, 'r') as f2:
            self.assertEqual(f2.read(), "# test2")

        # return to the original directory
        os.chdir(self.cwd)    

if __name__ == '__main__':
    unittest.main()
