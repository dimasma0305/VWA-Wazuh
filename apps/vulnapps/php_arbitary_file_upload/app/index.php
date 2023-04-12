<!DOCTYPE html>
<html lang="en">

<head>
    <base action>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="style.css">
    <title>Cloud Storage</title>
</head>

<body class="flex flex-col gap-10 w-screen h-screen max-h-screen items-center">
    <p class="text-6xl text-center">Cloud Storage</p>
    <div class="flex flex-col w-screen items-center">
        <div class="border border-white w-[20rem] p-10">
            <form action="upload.php" method="post" enctype="multipart/form-data" class="flex flex-col gap-2">
                <input type="file" name="file" id="file">
                <button type="submit">upload</button>
            </form>
        </div>
    </div>
    <div class="w-screen flex flex-col items-center h-[35%]">
        <div class="w-[50%] h-[80%] text-center overflow-auto">
            <?php
            $dir = "./files";
            if (is_dir($dir)) {
                if ($dh = opendir($dir)) {
                    while (($file = readdir($dh)) !== false) {
                        if (!str_starts_with($file, ".")) {
                            echo "<a href='files/$file'>$file</a> <br/>";
                        }
                    }
                    closedir($dh);
                }
            }
            ?>
        </div>
    </div>
    <div class="align-bottom text-center">php arbitary file upload</div>
</body>

</html>