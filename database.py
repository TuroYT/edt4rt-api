import mysql.connector
import os
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Class principale
class BDD:
  def __init__(self) -> None:
    
    try:
      self.__db = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        database=os.environ.get("DB_NAME")
      )
    
      logger.info("Connexion à la base de donnée réussie")
    except Exception as e:
      print(f"Erreur : {e}")
      logger.error(f"Erreur : {e}")
      
      
  def get_all_formations(self):
    """Recupère la liste des Formations de l'uppa

    Returns:
        dict[]: clefs = id, nom, description, lieux
    """

    cursor = self.__db.cursor()
    cursor.execute("SELECT * FROM `uppa_formation`;")
    result = cursor.fetchall()
    logger.info(f"Récupération de {len(result)} formations")
    
    res = []
    for i in result:
      res.append({
        "id":i[0],
        "nom":i[1],
        "description":i[2],
        "lieux":i[3]
      })

    
    cursor.close()
    return res
  
  def get_all_groupe(self):
    """get all groupes

    Returns:
        dict[]: key = id, nom, ics_link
    """
    
    cursor = self.__db.cursor()
    cursor.execute("SELECT * FROM `uppa_groupe`;")
    result = cursor.fetchall()
    to_return = []
    for i in result:
      to_return.append({
        "id":i[0],
        "nom":i[1],
        "ics_link":i[2]
      })
    logger.info(f"Récupération de {len(to_return)} groupes")
    cursor.close()
    return to_return
    
  def get_ics_link(self, id):
    """get ics link from id

    Args:
        id (int): id du groupe

    Returns:
        str: lien ics ou None
    """
    cursor = self.__db.cursor()
    cursor.execute("SELECT lien_ics FROM `uppa_groupe` WHERE id = %s;", (id,))
    result = cursor.fetchall()
    cursor.close()
    logger.info(f"Récupération du lien ics du groupe {id}")
    return result[0][0]

  def get_groups_from_formation(self, formation_id:int):
    """Recupere les groupes avec l'id de la formation

    Args:
        formation_id (int): formation id

    Returns:
        dict[]: id nom lien_ics
    """
    
    cursor = self.__db.cursor()
    query = "SELECT g.id, g.nom, g.lien_ics FROM uppa_groupe g INNER JOIN uppa_rel_formation_groupe fg ON g.id = fg.groupe_id WHERE fg.formation_id = %s"
    cursor.execute(query, (formation_id,))
    result = cursor.fetchall()
    cursor.close()
    return result