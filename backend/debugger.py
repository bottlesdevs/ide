import yaml


class Debugger():

    @staticmethod
    def validate_yaml(text):
        try:
            yaml.safe_load(text)
            return ''
        except yaml.YAMLError as exc:
            return exc