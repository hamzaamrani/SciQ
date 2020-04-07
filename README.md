# SciQ

Il nostro progetto consiste nello sviluppare un'applicazione che permetta il riconoscimento e la successiva risoluzione di formule matematiche simboliche. 
L'inserimento della formula può avvenire attraverso l'utilizzo di una text area oppure attraverso il caricamento di un'immagine,
mentre la risoluzione avviene mediante l'utilizzo delle API di Wolfram|Alpha.


Our project aim to develop an application that allow the recognition and further the resolution of symbolic mathematical formulas.
The insertion of the formulas could happen through the use of a predefined text-area or through the uploading of an image containing a formula.
The resolution of the formulas happen through the use of Wolphram|Alpha's API.

## Database
To use app:

`docker-compose up --build`, if there isn't a local DB mapped to volume the DB will be created

**on windows system the url isn't 0.0.0.0 but docker engine IP**

To perform test:

`docker-compose up -d --build && docker exec web python -m unittest -v tests.runner` or run bash file `test.sh` 

If there are changes in code `docker-compose up --build`
