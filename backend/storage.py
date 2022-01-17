import os


class FilesStorage:
    
    def __init__(self):
        self.files = {}
        self.current_file = None
    
    def add_file(self, file_name, file_content):
        '''
        Add a file to the storage
        '''
        self.files[file_name] = {
            'content': file_content,
            'modified': False,
            'path': file_name,
            'name': os.path.basename(file_name),
            'err': '',
            'changes': {} # TODO: not implemented yet
        }
    
    def get_file(self, file_name):
        return self.files[file_name]
    
    def get_files(self):
        return self.files
    
    def get_current_file(self):
        return self.current_file
    
    def set_current_file(self, file_name):
        self.current_file = file_name
    
    def remove_file(self, file_name):
        del self.files[file_name]
        if self.current_file == file_name:
            if len(self.files) > 0:
                self.current_file = list(self.files.keys())[0]
            else:
                self.current_file = None
    
    def remove_all_files(self):
        self.files = {}
    
    def is_file_opened(self, file_name):
        return file_name in self.files
    
    def is_file_modified(self, file_name):
        return self.files[file_name]['modified']
    
    def set_file_modified(self, file_name, modified):
        self.files[file_name]['modified'] = modified
    
    def set_file_err(self, file_name, err):
        self.files[file_name]['err'] = err
