# novel-crawler

## database sqls
##### CREATE TABLE `novel_book` (
##### `id` int(10) NOT NULL AUTO_INCREMENT,
#####  `site_name` varchar(255) NOT NULL,
#####  `book_name` varchar(255) NOT NULL,
#####  `author` varchar(255) DEFAULT NULL,
#####  `url` varchar(255) NOT NULL,
#####  `description` varchar(255) DEFAULT NULL,
#####  `book_type` varchar(255) DEFAULT NULL,
#####  `cover` varchar(255) DEFAULT NULL,
#####  `book_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
#####  `last_update_time` datetime DEFAULT NULL,
#####  `fetch_date` datetime DEFAULT NULL,
#####  PRIMARY KEY (`id`)
##### ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
##### CREATE TABLE `novel_chapter` (
#####  `id` int(10) NOT NULL AUTO_INCREMENT,
#####  `book_id` varchar(255) NOT NULL,
#####  `chapter_name` varchar(255) NOT NULL,
#####  `chapter_content` longtext,
#####  `chapter_url` varchar(255) NOT NULL,
#####  PRIMARY KEY (`id`)
##### ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
#### 
## crawl a single novel
##### scrapy crawl xbiquge -a book_name=牧神记
#### 
## crawl all novels
##### scrapy crawl xbiquge 
#### 
## othor args
##### -a update_books=False，是否更新已经抓取的小说
