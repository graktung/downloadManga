# Download Manga
Hỗ trợ download, tìm kiếm các bộ, tập truyện trên một số websites
## Chuẩn bị
Các bạn cần phải đáp ứng những thứ sau đây để có thể sử dụng được thư viện này.
### Môi trường
Version Python 3.X (3.6.1).         
Các bạn [Download Python ở đây](https://www.python.org/downloads/) để cài đặt nếu như đang sử dụng hệ điều hành Windows.
### Các module cần cài đặt thêm
* [jsbeautifier](https://github.com/beautify-web/js-beautify)        
Cài đặt bằng command sau:
```
pip install jsbeautifier
```
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/download           
Các bạn có thể down load về rồi chạy file `setup.py` bằng command sau:
```
python setup.py install
```
Nếu không, hãy cài đặt bằng cách sau:
```
pip install bs4
pip install lxml
```
* requests         
Cài đặt bằng command sau:
```
pip install requests
```
## Hỗ trợ các websites
Dưới đây là một số webistes được hỗ trợ.
### Hỗ trợ download trên các websites
* [http://blogtruyen.com/](http://blogtruyen.com/)
* [http://truyentranhtuan.com/](http://truyentranhtuan.com/)
* [http://www.mangapanda.com/](http://www.mangapanda.com/)
* [http://hentaivn.net/](http://hentaivn.net/)
* [http://manganel.com/](http://manganel.com/)
* [http://truyentranh8.net/](http://truyentranh8.net/)
### Hỗ trợ tìm kiếm trên các websites
* [http://manganel.com/](http://manganel.com/)
* [http://truyentranh8.net/](http://truyentranh8.net/)
## Cách sử dụng
Chạy file `main.py`
```
python main.py
```
Config file `database\configthreading.txt` để thay đổi threading. Tăng giảm tốc độ download và số lượng thread cho phép tối đa là **10**
## Command line
Các command line được sử dụng trong script
<table>
	<tbody>
		<tr>
			<th>load</th>
			<th>Chọn để download toàn bộ các tập truyện của một bộ truyện</th>
		</tr>
		<tr>
			<th>load only</th>
			<th>Chọn để download một tập truyện bất kì</th>
		</tr>
		<tr>
			<th>search</th>
			<th>Chọn để tìm kiếm truyện</th>
		</tr>
		<tr>
			<th>clear</th>
			<th>Xóa màn hình</th>
		</tr>
		<tr>
			<th>exit</th>
			<th>Dừng sử dụng script</th>
		</tr>
	</tbody>
</table>