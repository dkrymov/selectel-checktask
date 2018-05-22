<?php

$api_url = 'http://192.168.222.138:8000/api';

$tests = [
	[
		'call'			=> '/tickets',
		'params'	=> [
			'subject'	=> 'subject',
			'body'		=> 'dfgsdfgsdfg',
			'email'		=> 'mail@da.net'
		]
	],
	[
		'call'			=> '/tickets/1/comments',
		'params'	=> [
			'body'	=> 'comment 1',
			'email'	=> 'email@domain.com'
		]
	],
	[
		'call'			=> '/tickets/123/comments',
		'params'	=> [
			'body'	=> 'comment 123',
			'email'	=> 'email@domain.com'
		]
	],
	[ # 3
		'call'			=> '/tickets/1',
		'params'	=> [
			'status'	=> 'answered'
		]
	],
	[ # 4
		'call'			=> '/tickets/1',
		'params'	=> [
			'status'	=> 'opened'
		]
	],
	[ # 5
		'call'			=> '/tickets/1',
		'params'	=> null
	]
];

foreach ($tests as $test) {
	run_curl($api_url . $test['call'], $test['params']);
	#exit();
}

# editing db directly
$pdo = new PDO('pgsql:user=postgres host=192.168.222.138');
$pdo->query("update helpdesk.tickets set body = 'memcached test'");

# showing from memcache
$test = end($tests);
run_curl($api_url . $test['call'], $test['params']);

function run_curl($url, $params = null)
{
	$ch = curl_init();

	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

	if ($params) {
		curl_setopt($ch, CURLOPT_POST, 1);
		curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($params));
	}

	$server_output = curl_exec ($ch);

	print_r($server_output); echo "\n";

	curl_close ($ch);
}

