use Main;

INSERT INTO Branches VALUES (1, 'Happy Branch', 'Warszawa');
INSERT INTO Branches VALUES (2, 'Lucky Branch', 'Krakow');


use Main;
INSERT INTO Client VALUES ('Maciej Buba', 'Warszawa ul.Krakowska 5', 'maciejbubka@poczta.pl');
INSERT INTO Account VALUES (1,200.00, '1234567890', 'Standard');

INSERT INTO Client VALUES ('Andrzej Huba', 'Krakow ul.Warszawska 6', 'andrzejhubka@poczta.pl');
INSERT INTO Account VALUES (2,400.00, '1234567890', 'Standard');

INSERT INTO Client VALUES ('Paweł Skoczek', 'Warszawa ul.Wysoka 1', 'paweljumper@poczta.pl');
INSERT INTO Account VALUES (3,6000.00, '1234567890', 'Premium');

INSERT INTO Client VALUES ('Krzysztof Jarzyna', 'Szczecin ul.Morska 2', 'szef@poczta.pl');
INSERT INTO Account VALUES (4,400000.00, '1234567890', 'Premium++');

use Branch1;
INSERT INTO Client VALUES (1,'Maciej Buba', 'Warszawa ul.Krakowska 5', 'maciejbubka@poczta.pl');
INSERT INTO Account VALUES (1,1,200.00, '1234567890', 'Standard');

INSERT INTO Client VALUES (3,'Paweł Skoczek', 'Warszawa ul.Wysoka 1', 'paweljumper@poczta.pl');
INSERT INTO Account VALUES (3,3,6000.00, '1234567890', 'Premium');

use Main;
INSERT INTO Account_Branch VALUES (1,1);

use Branch2;
INSERT INTO Client VALUES (2,'Andrzej Huba', 'Krakow ul.Warszawska 6', 'andrzejhubka@poczta.pl');
INSERT INTO Account VALUES (2,2,400.00, '1234567890', 'Standard');

INSERT INTO Client VALUES (4,'Krzysztof Jarzyna', 'Szczecin ul.Morska 2', 'szef@poczta.pl');
INSERT INTO Account VALUES (4,4,400000.00, '1234567890', 'Premium++');

use Main;
INSERT INTO Account_Branch VALUES (2,2);
GO
