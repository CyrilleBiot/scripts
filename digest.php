<?php
#
# cyrille <cyrille@cbiot.fr>
# http://cbiot.fr/pedagogies-alternatives
# Licence GPL
#

# Debut du script
	$time_start = microtime(true);

# Recuperation des donnees de connexion		
	require'config.php';

# Nombre de jour à garder
	$nb_days = 7 ;

# Période à afficher 
	$today = date('d/m/Y', time()) ;
	$todayDiff =  date('d/m/Y',strtotime("- $nb_days days" ));	
	
# Message de présentation du mail
   $message  = 'Voici les nouveautés du forum depuis les '. $nb_days . ' jours ' . "\r\n \r\n"  ;
 
# Preparation de la connexion
	$DBconnect = "mysql:dbname=".$db_name.";host=".$db_host;

# Tentative de connexion pdo
try 	{
      $pdo = new PDO($DBconnect, $db_username, $db_password, array (PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES \'UTF8\''));

# =========================================
# RECUPERATION DES EMAIL ADMIN / WEBMASTER
# Du nom du forum et de l'url
# Sous la variable $mailToAdmin -> tableau
# [2] Admin et [3] Webmaster
# [0] Board Title et [1] Base Url
# =========================================
		# La requete avec ses clauses
		$sqlClause = 'FROM '.$db_prefix.'config WHERE conf_name LIKE \'o_admin_email\' OR conf_name LIKE \'o_webmaster_email\'' .
						 ' OR conf_name LIKE \'o_board_title\' OR conf_name LIKE \'o_base_url\' ';		
		
		# Test de la requete
		$sql = 'SELECT COUNT(*)' . $sqlClause ; 
			
		if ($res = $pdo->query($sql)) {

		# Test du nombre de lignes qui correspond à la requête SELECT COUNT
  		if ($res->fetchColumn() > 0) {

      		# Des résultats sont retournés , effectue la requête SELECT et travaille sur les résultats
    			  $sql = 'SELECT * ' . $sqlClause ;
    			  foreach ($pdo->query($sql) as $row) { # Affichage des résultats
						$globalData[] .= $row['conf_value'];
    			  } # fin du foreach		    
  				} else {	# Aucun résultat
     			echo 'Problème de configuration dans la structure du forum';
   			} # Fin du If Test resultat
}


# ===================================		
# RECUPERATION DES NOUVEAUX SUJETS		
# ===================================

		# La requete avec ses clauses
		$sqlClause = 'FROM '.$db_prefix.'topics WHERE CAST( FROM_UNIXTIME(last_post ) AS DATE)> DATE_SUB(now(), INTERVAL '.$nb_days.' DAY)' 
						. ' ORDER BY last_post DESC';	
		
		# Test de la requete
		$sql = 'SELECT COUNT(*)' . $sqlClause ; 
		
		if ($res = $pdo->query($sql)) {

		# Test du nombre de lignes qui correspond à la requête SELECT COUNT
  		if ($res->fetchColumn() > 0) {

      		# Des résultats sont retournés , effectue la requête SELECT et travaille sur les résultats
    			  $sql = 'SELECT * ' . $sqlClause ;
    			  $nbMsg = 0 ; 
    			  foreach ($pdo->query($sql) as $row) { # Affichage des résultats
    			  		$nbMsg++ ;
						$message .=  'De  '. $row['poster'] . "\r\n";
						$message .=   'Sujet : '. $row['subject'] . "\r\n";
						$message .=   'Posté : ' .date('m/d/Y', $row['posted']). ' --Dernière réponse le : '.date('m/d/Y', $row['last_post']) . "\r\n" ;
						$message .=  'Accèder au message : [ ' . $globalData[1] .'/viewtopic.php?pid='.$row['last_post_id'].'#p'.$row['last_post_id'] . ' ]';
						$message .= "\r\n". '----------------------------------------------------------------';							
						$message .= "\r\n \r\n";
    			  } # fin du foreach
    			  $message .= "\r\n". '----------------------------------------------------------------' . "\r\n";													
			     $message .= $globalData[0];
			     
  				} else {	# Aucun résultat
     			$message .= 'Aucune nouveauté dans le forum à ce jour \r\n \r\n';
     			$nbMsg = 0 ;
   			} # Fin du If Test resultat
}


# ===================================		
# GESTION DE L'ENVOI DES EMAILS		
# ===================================

# ===================================
	# Si membres ne souhaitant pas être dans le digest
	# leur adresse sont stockées dans un fichier txt
	# digest-blacklist.txt
	# Un membre par ligne avec une fausse entrée. Impératif !
	
	
	$filename_blacklist = 'digest-blacklist.txt';


	if (file_exists($filename_blacklist)) {
		$tab_bl = array();
		$fn = fopen($filename_blacklist,"r");
  			while(! feof($fn))  {
			$result = fgets($fn);
			array_push($tab_bl, $result);
  			}
		fclose($fn);

	# Recuperation element tableau
	foreach ($tab_bl as $arrayElement)
		$v .= "'" .str_replace(array("\r\n","\n"),'', $arrayElement)."', ";

		
	# Si le dernier caractère est un espace, une virgule,... , on le supprime
	$v = str_replace("'',","",$v);
	$v = rtrim($v, " ");
	$v = rtrim($v, ",");


	$v = preg_replace('[^A-Za-z0-9-]', '', $v);
	$blacklist = 'WHERE username NOT IN ('.$v.') ' ;  


   } else {
   $blacklist = '';
	}

   # Clause de la requete
   $sqlClause = ' FROM '.$db_prefix.'users '. $blacklist ;
		
	# Test de la requete
	$sql = 'SELECT COUNT(*)' . $sqlClause ; 		
   if ($res = $pdo->query($sql)) {

		# Test du nombre de lignes qui correspond à la requête SELECT COUNT
  		if ($res->fetchColumn() > 0) {

      		# Des résultats sont retournés , effectue la requête SELECT et travaille sur les résultats
    			  $sql = 'SELECT * ' . $sqlClause ;
    			  $nbUsers = 0;
    			  foreach ($pdo->query($sql) as $row) { # Affichage des résultats
    			  		$nbUsers++ ;
						# ENVOI DE L'EMAIL    			  
							$mailTo = $row['username'] . ' <'. $row['email'] .'>' ;
							$subject = 'Sujets hebdomadaires ('. $nbMsg . ') du forum PEDAGOGIES ALTERNATIVES du '. $todayDiff . ' au ' .$today ;
							$headers = 'From: ' . $globalData[2] . "\r\n" .
          							  'Reply-To: '.$globalData[2] . "\r\n" .
											'Content-type: text/plain; charset=UTF-8\r\n'. "\r\n" .
											'Content-Transfer-Encoding: 8bit' .
         							   'X-Mailer: PHP/' . phpversion();
							# ENVOI DU MAIL
							mail($mailTo, $subject, $message, $headers);	    			  
    			  			# POUR AFFICHAGE
    			  			$listMailTo .= $mailTo .' -- '; 			  
    			  
    			  } # fin du foreach
    			    
  				} else {	# Aucun résultat
     			echo "Aucun utilisateur enregistré. Pas normal, l'administrateur devrait être au moins présent... Vérifier vos tables...";
   			} # Fin du If Test resultat
	}

	# Cloture
	$pdo = null;
	$res = null ;	
	
# ============================================
# Sortie écran
# ============================================
	echo '<h1>GESTION DES MAILS</h1>';
	
	$messageToScreen = preg_replace('%(http[s]?://)(\S+)%', '<a href="\1\2" target="_blank">\1\2</a>', $message);

	# Fin du script
	$time_end = microtime(true);
	$time = $time_end - $time_start;

	echo 'Temps d\'execution du script : ' .  $time . ' secondes <br><br>';	
	echo '<b>Liste des destinataires ('.$nbUsers.') : </b>' . htmlentities($listMailTo) .  '  <br><br>';
	echo '<b>Sujet : </b>' . $subject .  '  <br><br>' ;
	echo '<b>voici le mail envoyé : </b><br><br>' ;	
	echo nl2br($messageToScreen).'' ;
	echo '<br><br><b>User(s) Blacklisté(s) : </b>'. $v ; 
	
	echo '<br><br><b>SQL : </b>'. $sql ; 

# Gestion ERREUR PDO
  } catch (PDOException $e) {
  print "Erreur De Connexion : " . $e->getMessage() . "<br/>";
  die();
  } # Fin du try
?>
