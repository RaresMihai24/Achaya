<?php
$servername = "db";
$username = "dragon_user";
$password = "dragon_pass";
$database = "dragon_db";

// Create connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Stabilim numele dragonului activ din formular sau selectăm unul implicit
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Extragem numele dragonului din orice acțiune
    foreach (['feed_dragon', 'water_dragon', 'play_dragon', 'groom_dragon', 'treat_dragon', 'sleep_dragon'] as $action) {
        if (isset($_POST[$action])) {
            $dragon_name = $conn->real_escape_string($_POST[$action]);
            break;
        }
    }

    // Dacă e acțiune de reproducere, folosim mama ca referință pentru afișare
    if (isset($_POST['mother']) && isset($_POST['father'])) {
        $dragon_name = $conn->real_escape_string($_POST['mother']); // sau poți lăsa gol
    }
} else {
    // Fără POST, selectăm un dragon implicit
    $default_result = $conn->query("SELECT name FROM dragons LIMIT 1");
    if ($default_result->num_rows > 0) {
        $default_dragon = $default_result->fetch_assoc();
        $dragon_name = $default_dragon['name'];
    }
}


// Dacă nu s-a trimis niciun formular, selectăm primul dragon din listă
if (!isset($_POST['feed_dragon']) && !isset($_POST['water_dragon']) && !isset($_POST['play_dragon']) &&
    !isset($_POST['groom_dragon']) && !isset($_POST['treat_dragon']) && !isset($_POST['sleep_dragon']) &&
    !isset($_POST['mother']) && !isset($_POST['father'])) {

    $default_result = $conn->query("SELECT name FROM dragons LIMIT 1");
    if ($default_result->num_rows > 0) {
        $default_dragon = $default_result->fetch_assoc();
        $dragon_name = $default_dragon['name'];
    }
}

if (!empty($dragon_name)) {
    $query = "SELECT race, specie, height, sex, age, weight, born_on, res, vit, dre, gal, sar, tra, GP, BLUP, mother, father, producer FROM dragons WHERE name = '$dragon_name'";
    $result = $conn->query($query);

    if ($result && $result->num_rows > 0) {
        $dragon = $result->fetch_assoc();
        $race = $dragon['race'];
        $specie = $dragon['specie'];
        $height = $dragon['height'];
        $sex = $dragon['sex'];
        $age = $dragon['age'];
        $weight = $dragon['weight'];
        $born_on = $dragon['born_on'];
        $breed_by = $dragon['producer'];
        $res = $dragon['res'];
        $vit = $dragon['vit'];
        $dre = $dragon['dre'];
        $gal = $dragon['gal'];
        $sar = $dragon['sar'];
        $tra = $dragon['tra'];
        $BLUP = $dragon['BLUP'];
        $mother = $dragon['mother'];
        $father = $dragon['father'];
        $GP = $res + $vit + $dre + $gal + $sar + $tra;
    } else {
        echo "Dragon not found.";
    }
}

// Fetch all dragons for selection
$result = $conn->query("SELECT name FROM dragons");
$dragons = $result->fetch_all(MYSQLI_ASSOC);
// Handle feeding process
if (isset($_POST['feed_dragon'])) {
    $energy_result = $conn->query("SELECT energy FROM dragons WHERE name = '$dragon_name'");

    if ($energy_result->num_rows > 0) {
        $row = $energy_result->fetch_assoc();
        $current_energy = floatval($row['energy']);
        $added_energy = 8;  // Example: You want to add 8 points

        // Add the specified value to the current energy
        $new_energy = min(100, round($current_energy + $added_energy, 2));

        // Update energy in DB
        $update_query = "UPDATE dragons SET energy = $new_energy WHERE name = '$dragon_name'";
        if ($conn->query($update_query) === TRUE) {
            echo "<p>Fed $dragon_name! Energy is now $new_energy.</p>";
        } else {
            echo "<p>Error updating energy: " . $conn->error . "</p>";
        }
    }
}

$query = "SELECT race, specie, height, sex, age, weight, born_on, res, vit, dre, gal, sar, tra, GP, BLUP, mother, father, producer FROM dragons WHERE name = '$dragon_name'";
$result = $conn->query($query);

if ($result->num_rows > 0) {
    $dragon = $result->fetch_assoc();
    $race = $dragon['race'];
    $specie = $dragon['specie'];
    $height = $dragon['height'];
    $sex = $dragon['sex'];
	$age = $dragon['age'];
    $weight = $dragon['weight'];
    $born_on = $dragon['born_on'];
    $breed_by = $dragon['producer'];  // Assuming 'producer' is the person who bred the dragon
	$res = $dragon['res'];
	$vit = $dragon['vit'];
	$dre = $dragon['dre'];
	$gal = $dragon['gal'];
	$sar = $dragon['sar'];
	$tra = $dragon['tra'];
	$BLUP = $dragon['BLUP'];
	$mother = $dragon['mother'];
	$father = $dragon['father'];
	$GP = $res + $vit + $dre + $gal + $sar + $tra;
} else {
    echo "Dragon not found.";
}


// Handle watering process
if (isset($_POST['water_dragon'])) {
    $stats_result = $conn->query("SELECT energy, moral FROM dragons WHERE name = '$dragon_name'");

    if ($stats_result->num_rows > 0) {
        $row = $stats_result->fetch_assoc();
        $current_energy = floatval($row['energy']);
        $current_moral = floatval($row['moral']);

        $added_energy = 2;  // Example: You want to add 2 points of energy
        $added_moral = 1;   // Example: You want to add 1 point of moral

        // Add the specified values to the current energy and moral
        $new_energy = min(100, round($current_energy + $added_energy, 2));
        $new_moral = min(100, round($current_moral + $added_moral, 2));

        // Update values in the DB
        $update_query = "UPDATE dragons SET energy = $new_energy, moral = $new_moral WHERE name = '$dragon_name'";
        if ($conn->query($update_query) === TRUE) {
            echo "<p>Gave water to $dragon_name! Energy is now $new_energy, Moral is now $new_moral.</p>";
        } else {
            echo "<p>Error updating stats: " . $conn->error . "</p>";
        }
    }
}

// Handle play process
if (isset($_POST['play_dragon'])) {
    $energy_result = $conn->query("SELECT energy FROM dragons WHERE name = '$dragon_name'");

    if ($energy_result->num_rows > 0) {
        $row = $energy_result->fetch_assoc();
        $current_energy = floatval($row['energy']);

        $added_energy = 5;  // Example: You want to add 5 points of energy
        $new_energy = min(100, round($current_energy + $added_energy, 2));

        $update_query = "UPDATE dragons SET energy = $new_energy WHERE name = '$dragon_name'";
        if ($conn->query($update_query) === TRUE) {
            echo "<p>You played with $dragon_name! Energy is now $new_energy.</p>";
        } else {
            echo "<p>Error updating energy: " . $conn->error . "</p>";
        }
    }
}

// Handle grooming process
if (isset($_POST['groom_dragon'])) {
    $moral_result = $conn->query("SELECT moral FROM dragons WHERE name = '$dragon_name'");

    if ($moral_result->num_rows > 0) {
        $row = $moral_result->fetch_assoc();
        $current_moral = floatval($row['moral']);

        $added_moral = 3;  // Example: You want to add 3 points of moral
        $new_moral = min(100, round($current_moral + $added_moral, 2));

        $update_query = "UPDATE dragons SET moral = $new_moral WHERE name = '$dragon_name'";
        if ($conn->query($update_query) === TRUE) {
            echo "<p>You groomed $dragon_name! Moral is now $new_moral.</p>";
        } else {
            echo "<p>Error updating moral: " . $conn->error . "</p>";
        }
    }
}

// Handle giving treat process
if (isset($_POST['treat_dragon'])) {
    $energy_result = $conn->query("SELECT energy FROM dragons WHERE name = '$dragon_name'");

    if ($energy_result->num_rows > 0) {
        $row = $energy_result->fetch_assoc();
        $current_energy = floatval($row['energy']);

        $added_energy = 10;  // Example: You want to add 10 points of energy
        $new_energy = min(100, round($current_energy + $added_energy, 2));

        $update_query = "UPDATE dragons SET energy = $new_energy WHERE name = '$dragon_name'";
        if ($conn->query($update_query) === TRUE) {
            echo "<p>You gave a treat to $dragon_name! Energy is now $new_energy.</p>";
        } else {
            echo "<p>Error updating energy: " . $conn->error . "</p>";
        }
    }
}


if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['sleep_dragon'])) {
        // Update the 'sleep' field in the database to 'YES' for the selected dragon
        $update_query = "UPDATE dragons SET sleep = 'YES' WHERE name = '$dragon_name'";
        if ($conn->query($update_query) === TRUE) {
            echo "<p>$dragon_name is now sleeping.</p>";
        } else {
            echo "<p>Error updating sleep status: " . $conn->error . "</p>";
        }

        // Redirect to the same page to see the updated information
        header("Location: " . $_SERVER['REQUEST_URI']);
        exit();
    }
}

// Handle breeding process

if (isset($_POST['mother']) && isset($_POST['father']) && isset($_POST['foal_name'])) {
    $mother_name = $conn->real_escape_string($_POST['mother']);
    $father_name = $conn->real_escape_string($_POST['father']);
    $foal_name = $conn->real_escape_string($_POST['foal_name']);
    
    // Fetch parent details
    $mother_result = $conn->query("SELECT * FROM dragons WHERE name = '$mother_name'");
    $father_result = $conn->query("SELECT * FROM dragons WHERE name = '$father_name'");

    if ($mother_result->num_rows > 0 && $father_result->num_rows > 0) {
        $mother = $mother_result->fetch_assoc();
        $father = $father_result->fetch_assoc();

        // Assign random sex
        $sex = (rand(0, 1) == 0) ? "Mascul" : "Femela";

        // Assign race from parents
        $race = $mother['race'];

        // Assign random weight and height
        $weight = rand(5, 10);
        $height = rand(15, 20);

        // Set species
        $specie = "Soparla cu aripi";

        // Helper functions for calculations
        function calculateAverage($mother_stat, $father_stat) {
            return ($mother_stat + $father_stat) / 2;
        }

        function applyBLUPInfluence($average_stat, $mother_blup, $father_blup) {
            $blup_influence = ($mother_blup + $father_blup) / 2;
            return $average_stat + $blup_influence;
        }

        function applyImprovementFactor($final_stat, $mother_stat, $father_stat) {
            return ($mother_stat == $father_stat) ? $final_stat * 1.05 : $final_stat;
        }

        function calculateStat($mother_stat, $father_stat, $mother_blup, $father_blup) {
            $mother_stat = floatval($mother_stat);
            $father_stat = floatval($father_stat);
            $mother_blup = floatval($mother_blup);
            $father_blup = floatval($father_blup);

            $average_stat = calculateAverage($mother_stat, $father_stat);
            $final_stat = applyBLUPInfluence($average_stat, $mother_blup, $father_blup);
            $final_stat = applyImprovementFactor($final_stat, $mother_stat, $father_stat);
            return max(0, round($final_stat, 2)); // Ensuring no negative values and rounding to 2 decimal places
        }

        // Get BLUP values for the parents
        $mother_blup = floatval($mother['BLUP']);
        $father_blup = floatval($father['BLUP']);

        // Calculate the offspring's stats
        $new_res = calculateStat($mother['res'], $father['res'], $mother_blup, $father_blup);
        $new_vit = calculateStat($mother['vit'], $father['vit'], $mother_blup, $father_blup);
        $new_dre = calculateStat($mother['dre'], $father['dre'], $mother_blup, $father_blup);
        $new_gal = calculateStat($mother['gal'], $father['gal'], $mother_blup, $father_blup);
        $new_sar = calculateStat($mother['sar'], $father['sar'], $mother_blup, $father_blup);
        $new_tra = calculateStat($mother['tra'], $father['tra'], $mother_blup, $father_blup);

        // Get today's date for born_on
        $born_on = date('Y-m-d');
		// Calculate GP as the sum of all base attributes
		$GP = $new_res + $new_vit + $new_dre + $new_gal + $new_sar + $new_tra;

// Function to calculate ac_ stats based on BLUP influence
function calculateAcStat($base_stat, $blup_avg) {
    // Smooth scaling formula (max 14-15% at 100 BLUP avg)
    $percent = 0.15 * ($blup_avg / (100 + $blup_avg)); 
    
    return round($base_stat * $percent, 2);
}

// Calculate BLUP average
$blup_avg = ($mother_blup + $father_blup) / 2;

if ($mother_blup < 0 || $father_blup < 0) {
    $ac_res = $ac_vit = $ac_dre = $ac_gal = $ac_sar = $ac_tra = 0;
} else {
    // Compute each ability stat using the formula
    $ac_res = calculateAcStat($new_res, $blup_avg);
    $ac_vit = calculateAcStat($new_vit, $blup_avg);
    $ac_dre = calculateAcStat($new_dre, $blup_avg);
    $ac_gal = calculateAcStat($new_gal, $blup_avg);
    $ac_sar = calculateAcStat($new_sar, $blup_avg);
    $ac_tra = calculateAcStat($new_tra, $blup_avg);
}
        // Insert new baby dragon
	$insert_query = "
		INSERT INTO dragons (name, specie, producer, weight, height, age, born_on, sex, race, energy, health, moral, 
			res, vit, dre, gal, sar, tra, ac_res, ac_vit, ac_dre, ac_gal, ac_sar, ac_tra, GP, mother, father)
		VALUES ('$foal_name', '$specie', 'admin', $weight, $height, 'a few hours', '$born_on', '$sex', '$race', 
			100, 100, 100, $new_res, $new_vit, $new_dre, $new_gal, $new_sar, $new_tra, 
			$ac_res, $ac_vit, $ac_dre, $ac_gal, $ac_sar, $ac_tra, $GP, '$mother_name', '$father_name')
	";

        if ($conn->query($insert_query) === TRUE) {
            echo "New dragon '$foal_name' created successfully!";
        } else {
            echo "Error: " . $insert_query . "<br>" . $conn->error;
        }
    }
}
?>

<script>
// JavaScript for tab switching functionality
function showTab(tabName) {
    // Hide all tab content
    var contents = document.querySelectorAll('.tab-content');
    for (var i = 0; i < contents.length; i++) {
        contents[i].style.display = 'none';
    }

    // Show the clicked tab content
    var activeTab = document.getElementById(tabName);
    activeTab.style.display = 'block';

    // Set all tabs to inactive
    var tabs = document.querySelectorAll('.tab');
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].classList.remove('active');
    }

    // Set the clicked tab to active
    event.target.classList.add('active');
}

// By default, show the Characteristics tab
document.addEventListener('DOMContentLoaded', function() {
    showTab('characteristics');
});
</script>