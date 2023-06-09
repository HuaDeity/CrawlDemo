# CrawlDemo  

[中文说明](https://github.com/HuaDeity/CrawlDemo/blob/main/docs/中文说明.md)  

This is a demonstration of how to crawl images.

## Features

- Automate web crawling to retrieve images and flip pages automatically on a website.

- Add support for multiple browsers.

## Installation

### Requirements

Python 3.7+  
Chrome / Firefox / Edge / Safari  

### Install

```bash
git clone https://github.com/HuaDeity/CrawlDemo.git
cd CrawlDemo
pip install -r requirements.txt
```

## Usage

```bash
cd millitary
scrapy crawl gettyimages -a search_term=aircraftcarrier -a page_number=3 -a browser=chrome
scrapy crawl baidu -a search_term=航空母舰 -a image_number=10000 -a browser=chrome
```

In order to retrieve a specific image, the user must provide the following information:

- Website (gettyimages/alamy/google/baidu)

- Search term (keyword)

- Desired page number / image number (for baidu only)

- Preferred web browser (chrome/firefox/edge/safari)

The websites support now:  

- [GettyImages](https://gettyimages.com/)

- [Alamy](https://alamy.com/)

- [Google](https://google.com/imghp)

- [Baidu](https://image.baidu.com/)

## Tips  

- [GettyImages](https://gettyimages.com/) may need to change the keyword appropriately when searching in different regions, such as adding hyphens to get different search results.

- [Alamy](https://alamy.com/) images require a uniform crop of approximately 20px from the bottom.

- The spider disabled [Baidu](https://image.baidu.com/)'s robots.txt file due to its anti-crawling mechanism, which may violate the website's terms of service.  

## Comparison of Download Speeds

- Both [Google](https://google.com/imghp) and [Baidu](https://image.baidu.com/) are streaming websites that eliminate page loading time.  

- [GettyImages](https://gettyimages.com/) uses regular pagination mode.  

- [Alamy](https://alamy.com/) need to wait for webpage images to load, the speed is relatively slow.

## FAQ

1. To avoid [Gettyimages](https://gettyimages.com/) restricting access to your IP, it's advisable to reduce your crawling frequency. If you're still unable to download, consider changing your IP or waiting for a while before trying again.

## Contributing

Contributions are welcome! Please refer to our CONTRIBUTING.md for details on how to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/HuaDeity/CrawlDemo/blob/main/LICENSE) file for details.

## Contact

HuaDeity  
[Email](mailto:wangyizun@mail.nwpu.edu.cn)
