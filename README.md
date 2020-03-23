# SciQ

Il nostro progetto consiste nello sviluppare un'applicazione che permetta il riconoscimento e la successiva risoluzione di formule matematiche simboliche. 
L'inserimento della formula può avvenire attraverso l'utilizzo di una text area oppure attraverso il caricamento di un'immagine,
mentre la risoluzione avviene mediante l'utilizzo delle API di Wolfram|Alpha.


Our project aim to develop an application that allow the recognition and further the resolution of symbolic mathematical formulas.
The insertion of the formulas could happen through the use of a predefined text-area or through the uploading of an image containing a formula.
The resolution of the formulas happen through the use of Wolphram|Alpha's API.

## Database
To perform db creation/migration is necessary to execute follwing commands:
* `flask db init` (only for creation)
* `flask db migrate`
* `flask db upgrade`

To cleaning existing data and create new tables perform:
* `flask reset-db`

`flask --help` to show all possible command with description