<div align="center">
<h1> Yoworld Item API SDK </h1>
</div>

# Introducing our API documentation!

Here we host muliple endpoints for developers to create such yoworld tools and distribute them to the community

### Item Search
Endpoint: ``/search``
GET Parameters: ``q``

GET Request Example using cURL
```
curl -s 'https://api.yoworld.site/search?q=257460'
```

GET Request Example using Python
```
results = requests.get("https://api.yoworld.site/search?q=257460)
print(results.text)
```

### Advance Item Information
Endpoint: ``/advance``
GET Parameters: ``q``

GET Request Example using cURL
```
curl -s 'https://api.yoworld.site/advance?q=257460'
```

GET Request Example using Python
```
results = requests.get("https://api.yoworld.site/advanced?q=257460)
print(results.text)
```