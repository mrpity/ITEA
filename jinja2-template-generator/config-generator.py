#Import necessary functions from Jinja2 module
from jinja2 import Environment, FileSystemLoader

#Import YAML module
import yaml


if __name__ == '__main__':

    #Load data from YAML into Python dictionary
    config_data = yaml.load(open('./data_files/data_to_feed.yml'))

    #Load Jinja2 template
    env = Environment(loader = FileSystemLoader('./templates'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('template.txt')

    #Render the template with data and print the output
    print(template.render(config_data))

