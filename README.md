# CrawlDemo

This is a demo of image crawling.

## Features

- Automate web crawling by retrieving images from website and flipping pages automatically.  
- Support multiple browsers.

## Installation

### Requirements

Python 3.7+  
Chrome/Firefox/Edge/Safari

### Install

```bash
pip install -r requirements.txt
```

## Usage

```bash
git clone https://github.com/HuaDeity/CrawlDemo.git
cd CrawlDemo
cd millitary
scrapy crawl gettyimages -a search_term=aircraftcarrier -a page_number=3 -a browser=chrome
```

To retrieve a specific image, the user needs to provide three pieces of information: the search term (keyword), the desired page number, and their preferred web browser(chrome/firefox/edge/safari).  

The website support now:  

- [GettyImages](https://gettyimages.com/)
- [Alamy](https://alamy.com/)

## Contributing

Contributions are welcome! Please refer to our CONTRIBUTING.md for details on how to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/HuaDeity/CrawlDemo/blob/main/LICENSE) file for details.

## Contact

Yizun Wang  
[Email](mailto:wangyizun@mail.nwpu.edu.cn)
