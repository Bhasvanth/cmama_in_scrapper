# -*- coding: utf-8 -*-
import scrapy


class ExtractorSpider(scrapy.Spider):
    name = 'extractor'
    allowed_domains = ['cmama.in']
    start_urls = ['http://cmama.in']

    def parse(self, response):
        for lang_url  in response.css('ul.menu-first li a::attr(href)'):
        #     print "sub page ***********************************"
#            yield {'pdf_url' : pdf_url}
              print lang_url.extract()
              url = "".join([self.start_urls[0], lang_url.extract()])
              yield response.follow(url, self.parse_sub_pages, dont_filter = True)

    def parse_sub_pages(self, response):
        for url in response.css('div.portfolio-thumb a::attr(href)'): 
            print (url.extract())
            url = "".join([self.start_urls[0], url.extract()])
            #url  = response.urljoin(url.extract)
            #yield scrapy.Request(url, callback=self.parse_pdf_urls, dont_filter = True)
            yield response.follow(url, self.parse_pdf_urls, dont_filter = True)

    def parse_pdf_urls (self, response) :
        print response
        for url in response.css('div.article-row a::attr(href)')  :
            #yield {"url" : url.extract().split("?")[1].split("&")[0].split("=")[1]}
            if "file" in url.extract():
                pdf_url = url.extract().split("?")[1].split("&")[0].split("=")[1]
            else : 
                pdf_url = url.extract()
            yield scrapy.Request(
                url=response.urljoin(pdf_url),
                callback=self.save_pdf,
                dont_filter = True
            )

    def save_pdf(self, response):
        languageArr = ["english", "telugu", "hindi", "sanskrit", "bengali", "odia", "kannada", "marathi", "tamil"]
        language = ""
        for lang in languageArr :
            if lang in response.url :
                language = lang 
        path = "/".join(["../resources", language, response.url.split('/')[-1]])
        self.logger.info('Saving PDF %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)
