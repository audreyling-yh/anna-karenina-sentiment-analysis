import requests

class Puller:
    def __init__(self, url, output_filename):
        self.url = url
        self.output_filename = output_filename
        self.res = None

    def run(self):
        self.pull()
        self.export()

    def pull(self):
        self.res = requests.get(self.url)
        print(self.res.status_code)

    def export(self):
        html = self.res.content.decode('utf-8')
        filepath = '../data/raw/{}.html'.format(self.output_filename)
        with open(filepath, 'w') as file:
            file.write(html)

if __name__ == '__main__':
    url = 'https://www.gutenberg.org/files/1399/1399-h/1399-h.htm'
    output_name = 'anna-karenina'
    ws = Puller(url, output_name)
    ws.run()
