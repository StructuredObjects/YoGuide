<?php

require_once __DIR__ . '/router.php';


get('/', 'views/home');

post('/','views/results');
