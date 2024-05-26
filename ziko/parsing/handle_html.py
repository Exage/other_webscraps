from links import ziko_link, urls

def handle_html(html, url):
    products = html.find_all('div', 'product')
    handled_data = []

    for product in products:

        name = product.select_one('div.productColText span.middle').text
        
        price = product.select_one('div.productColText a.price').text
        price = price.replace('\t', '').replace('\n', '').split(' руб.')[0]

        link = product.select_one('a.btn-simple.add-cart').get('href')

        handled_data.append({
            'name': name,
            'price': price,
            'link': ziko_link + link,
            'url_numb': urls.index(url) + 1
        })
    
    return handled_data