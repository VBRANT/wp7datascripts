<?php

/*****************************************************
 *
 * Sample code to test GoldenGATE web services.
 * 
 * David King <David.King@open.ac.uk>
 * for the ViBRANT project <http://vbrant.eu>
 * September 2012
 *
 * License: GPLv2 <http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt>
 *
 ****************************************************/

function http_get($url) {
    $c = curl_init();
    curl_setopt($c, CURLOPT_URL, $url);
    curl_setopt ($c, CURLOPT_RETURNTRANSFER, true);
    return curl_exec($c);
}

function http_post($url, $post) {
    $c = curl_init();
    curl_setopt($c, CURLOPT_URL, $url);
    curl_setopt($c, CURLOPT_POST, true);
    curl_setopt($c, CURLOPT_POSTFIELDS, $post);
    curl_setopt ($c, CURLOPT_RETURNTRANSFER, true);
    return curl_exec($c);
}

echo "hello from GgWS test\n";

$service_path = 'http://localhost:8080';

$contents = "Mary had a little lamb at 52° 2' 18.96 north and 0° 45' 25.46 west";
$fields = array('responseFormat' => 'txt',
    'functionName' => 'GeoCoordinateTaggerNormalizing.webService',
    'dataFormat' => 'TXT',
    'INTERACTIVE' => 'no',
    'data' => $contents);

$initiate_request = http_post($service_path . '/GgWS/ws/invokeFunction', http_build_query($fields));

if ($initiate_request == '') {
    echo "no response from GgWS\n";
    echo "goodbye from GgWS test\n";
    exit(4);
} else {
    $response = simplexml_load_string($initiate_request);
    $running = true;
    while ($running == true)  {
        echo "{$response['stateDetail']}\n";
        switch($response['state']) {
            case 'Started':
            case 'Running':
                sleep(5);
                $response = simplexml_load_string((http_get($service_path . $response->callback[0])));
                break;
            case 'Finished':
                $result = http_get($service_path . $response->callback[1]);
                echo "{$result}\n";
                $running = false;
                break;
            default:
                echo "How did we get here?\n";
                echo "{$response}\n";
                $running = false;
        }
    }
}

echo "goodbye from GgWS test\n";

?>
