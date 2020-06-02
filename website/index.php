
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <link href="https://fonts.googleapis.com/css?family=Montserrat&display=swap" rel="stylesheet">
  <link href="./fontawesome-free-5.13.0-web/css/all.css" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.20/css/jquery.dataTables.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.js"></script>
  <script src="Javascript/ataskaitos.js"></script>
  <link rel="stylesheet" type="text/css" href="stylesheets/index.css">
  <link rel="stylesheet" type="text/css" href="stylesheets/table.css">
  <title>Sudoku LeaderBoard</title>
</head>

<body>
  <?php include("header.html"); ?>
  <?php include("error.php"); ?>
    <div class="paimtosKnygosTable">
      <table class="middleTable" id="mainTable">
        <thead>
          <tr>
            <th onclick="changeArrowDirection(0)">Skaitytojas   <i class="fas fa-long-arrow-alt-down" name="arrowDown0" style="display: none;"></i> <i class="fas fa-long-arrow-alt-up" name="arrowUp0"  style="display: none;"></i></th>
            <th onclick="changeArrowDirection(1)">Knyga   <i class="fas fa-long-arrow-alt-down" id="hideOnLoad" name="arrowDown1" style="display: none;"></i> <i class="fas fa-long-arrow-alt-up" id="hideOnLoad" name="arrowUp1" style="display: none;"></i></th>
            <th onclick="changeArrowDirection(2)">Paėmė    <i class="fas fa-long-arrow-alt-down" id="hideOnLoad" name="arrowDown2" style="display: none;"></i> <i class="fas fa-long-arrow-alt-up" id="hideOnLoad" name="arrowUp2" style="display: none;"></i></th>
            <th onclick="changeArrowDirection(3)">Grąžins   <i class="fas fa-long-arrow-alt-down" id="hideOnLoad" name="arrowDown3" style="display: none;"></i> <i class="fas fa-long-arrow-alt-up" id="hideOnLoad" name="arrowUp3" style="display: none;"></i></th>
          </tr>
        </thead>
        <tbody>
        </tbody>
      </table>
    </div>
</body>
</html>
</body>
</html>