/* Usuario */
INSERT INTO main_user (id, password, is_superuser, username, first_name, last_name, email, is_staff, is_active, identity_card, phone_number, user_type, institution, created_by, updated_by, date_joined, date_updated) VALUES
(1, 'pbkdf2_sha256$36000$dhqxoejz7cPU$y2UArD3//0+1ltQlMfeUM7NTK5oY/76FHD4YxquLg7o=', true, 'admin', 'Oswaldo', 'Bayona', 'admin@example.com', true, true, '0923333736', '0969455119', 1, 'ESPOL', 'Fernando Sánchez', 'Fernando Sánchez', current_timestamp, current_timestamp)
(2, 'pbkdf2_sha256$36000$dhqxoejz7cPU$y2UArD3//0+1ltQlMfeUM7NTK5oY/76FHD4YxquLg7o=', false, 'investigador', 'Carlos', 'Manosalvas', 'researcher@example.com', false, true, '0920335567', '0984487328', 2, 'ESPOL', 'Fernando Sánchez', 'Fernando Sánchez', current_timestamp, current_timestamp);
(3, 'pbkdf2_sha256$36000$dhqxoejz7cPU$y2UArD3//0+1ltQlMfeUM7NTK5oY/76FHD4YxquLg7o=', false, 'cliente', 'Fernando', 'Sanchez', 'customer@example.com', false, true, '0929858736', '0969488119', 3, 'UEES', 'Fernando Sánchez', 'Fernando Sánchez', current_timestamp, current_timestamp)

/* Gauging */
INSERT INTO simulation_gauging (date, weather, station, ts, te) VALUES ('2018-11-14', 'Normal', 'Semaforo del Km. 1.5 Av. Nicolas Lapenti y Av. Jaime Nebot, Duran', '07:00:00', '08:00:00')

/* Periodos */
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 1, '07:00:00', '07:15:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 2, '07:00:00', '07:15:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 3, '07:00:00', '07:15:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 4, '07:00:00', '07:15:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 5, '07:00:00', '07:15:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 6, '07:00:00', '07:15:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 7, '07:00:00', '07:15:00');

INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 8, '07:15:00', '07:30:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 9, '07:15:00', '07:30:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 10, '07:15:00', '07:30:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 11, '07:15:00', '07:30:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 12, '07:15:00', '07:30:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 13, '07:15:00', '07:30:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 14, '07:15:00', '07:30:00');

INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 15, '07:30:00', '07:45:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 16, '07:30:00', '07:45:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 17, '07:30:00', '07:45:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 18, '07:30:00', '07:45:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 19, '07:30:00', '07:45:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 20, '07:30:00', '07:45:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 21, '07:30:00', '07:45:00');

INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 22, '07:45:00', '08:00:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 23, '07:45:00', '08:00:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 24, '07:45:00', '08:00:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 25, '07:45:00', '08:00:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 26, '07:45:00', '08:00:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 27, '07:45:00', '08:00:00');
INSERT INTO simulation_term (gauging_id, number, ts, te) VALUES (1, 28, '07:45:00', '08:00:00');

/* Vehicle */
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (1, 1, 1, 16);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (1, 1, 2, 2);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (1, 2, 1, 89);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (1, 2, 2, 19);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (1, 3, 1, 12);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (1, 3, 2, 4);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (2, 1, 1, 16);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (2, 1, 2, 2);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (2, 2, 1, 80);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (2, 2, 2, 19);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (2, 3, 1, 12);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (2, 3, 2, 4);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (3, 1, 1, 13);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (3, 1, 2, 0);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (3, 2, 1, 71);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (3, 2, 2, 18);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (3, 3, 1, 16);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (3, 3, 2, 0);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (4, 1, 1, 9);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (4, 1, 2, 0);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (4, 2, 1, 60);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (4, 2, 2, 15);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (4, 3, 1, 21);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (4, 3, 2, 2);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (5, 1, 1, 16);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (5, 1, 2, 0);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (5, 2, 1, 38);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (5, 2, 2, 10);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (5, 3, 1, 25);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (5, 3, 2, 1);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (6, 1, 1, 20);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (6, 1, 2, 0);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (6, 2, 1, 70);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (6, 2, 2, 20);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (6, 3, 1, 22);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (6, 3, 2, 2);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (7, 1, 1, 21);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (7, 1, 2, 0);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (7, 2, 1, 60);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (7, 2, 2, 12);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (7, 3, 1, 21);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (7, 3, 2, 0);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (8, 1, 1, 14);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (8, 1, 2, 0);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (8, 2, 1, 61);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (8, 2, 2, 10);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (8, 3, 1, 20);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (8, 3, 2, 1);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (9, 1, 1, 18);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (9, 1, 2, 0);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (9, 2, 1, 71);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (9, 2, 2, 14);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (9, 3, 1, 19);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (9, 3, 2, 2);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (10, 1, 1, 17);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (10, 1, 2, 1);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (10, 2, 1, 65);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (10, 2, 2, 10);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (10, 3, 1, 22);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (10, 3, 2, 2);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (11, 1, 1, 19);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (11, 1, 2, 2);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (11, 2, 1, 60);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (11, 2, 2, 0);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (11, 3, 1, 17);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (11, 3, 2, 2);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (12, 1, 1, 20);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (12, 1, 2, 0);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (12, 2, 1, 65);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (12, 2, 2, 9);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (12, 3, 1, 15);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (12, 3, 2, 0);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (13, 1, 1, 17);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (13, 1, 2, 1);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (13, 2, 1, 82);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (13, 2, 2, 5);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (13, 3, 1, 14);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (13, 3, 2, 1);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (14, 1, 1, 16);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (14, 1, 2, 0);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (14, 2, 1, 70);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (14, 2, 2, 10);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (14, 3, 1, 15);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (14, 3, 2, 1);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (15, 1, 1, 12);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (15, 1, 2, 0);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (15, 2, 1, 58);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (15, 2, 2, 11);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (15, 3, 1, 8);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (15, 3, 2, 1);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (16, 1, 1, 11);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (16, 1, 2, 1);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (16, 2, 1, 60);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (16, 2, 2, 10);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (16, 3, 1, 20);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (16, 3, 2, 1);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (17, 1, 1, 10);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (17, 1, 2, 0);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (17, 2, 1, 50);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (17, 2, 2, 12);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (17, 3, 1, 19);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (17, 3, 2, 2);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (18, 1, 1, 8);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (18, 1, 2, 0);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (18, 2, 1, 78);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (18, 2, 2, 7);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (18, 3, 1, 10);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (18, 3, 2, 3);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (19, 1, 1, 12);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (19, 1, 2, 1);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (19, 2, 1, 60);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (19, 2, 2, 8);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (19, 3, 1, 8);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (19, 3, 2, 2);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (20, 1, 1, 15);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (20, 1, 2, 1);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (20, 2, 1, 130);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (20, 2, 2, 15);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (20, 3, 1, 0);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (20, 3, 2, 0);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (21, 1, 1, 8);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (21, 1, 2, 2);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (21, 2, 1, 105);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (21, 2, 2, 16);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (21, 3, 1, 20);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (21, 3, 2, 2);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (22, 1, 1, 13);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (22, 1, 2, 2);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (22, 2, 1, 90);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (22, 2, 2, 9);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (22, 3, 1, 15);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (22, 3, 2, 3);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (23, 1, 1, 11);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (23, 1, 2, 2);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (23, 2, 1, 120);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (23, 2, 2, 18);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (23, 3, 1, 12);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (23, 3, 2, 4);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (24, 1, 1, 6);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (24, 1, 2, 0);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (24, 2, 1, 60);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (24, 2, 2, 7);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (24, 3, 1, 22);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (24, 3, 2, 2);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (25, 1, 1, 14);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (25, 1, 2, 2);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (25, 2, 1, 70);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (25, 2, 2, 11);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (25, 3, 1, 16);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (25, 3, 2, 3);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (26, 1, 1, 10);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (26, 1, 2, 0);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (26, 2, 1, 65);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (26, 2, 2, 8);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (26, 3, 1, 19);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (26, 3, 2, 2);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (27, 1, 1, 15);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (27, 1, 2, 1);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (27, 2, 1, 55);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (27, 2, 2, 9);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (27, 3, 1, 15);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (27, 3, 2, 2);

INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (28, 1, 1, 10);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (28, 1, 2, 1);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (28, 2, 1, 61);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (28, 2, 2, 12);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (28, 3, 1, 18);
INSERT INTO simulation_vehicle (term_id, movement, type, number) VALUES (28, 3, 2, 1);
