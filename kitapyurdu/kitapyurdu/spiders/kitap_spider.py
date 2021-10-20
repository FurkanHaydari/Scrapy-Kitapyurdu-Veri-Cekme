import scrapy

class kitapSpider(scrapy.Spider):
    name = "kitaplar"
    page_count = 0
    book_count = 1
    file = open("okunacak_listesi.txt","a",encoding="UTF-8")
    start_urls = [ 
        "https://www.kitapyurdu.com/index.php?route=product/bestseller_ten_year&page=1"
    ]

    def parse(self, response):
        kitap_ismi = response.css("div.name.ellipsis a span::text").extract()
        kitap_yazar= response.css("div.author span a span::text").extract()
        yayinevi = response.css("div.publisher span a span::text").extract()

        i=0
        while (i<len(kitap_ismi)):
            self.file.write("-----------------------------------------------------------\n")
            self.file.write(str(self.book_count) + ".\n")
            self.file.write("Kitap ismi: " + kitap_ismi[i] + "\n")
            self.file.write("Yazar: " + kitap_yazar[i] + "\n")
            self.file.write("Yayınevi: " + yayinevi[i] + "\n")
            self.book_count +=1
            self.file.write("-----------------------------------------------------------\n") 
            i+=1
    
        next_url = response.css("a.next::attr(href)").extract_first()
        self.page_count+=1
        
        if next_url is not None and self.page_count != 5:
            yield scrapy.Request(url=next_url, callback=self.parse)
        else:
            self.file.close()