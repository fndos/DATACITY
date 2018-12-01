/*
Trigger que llena el campo ts_index antes de un insert o update
en la tabla Layer_layer
*/
CREATE TRIGGER tsvector_update_layer BEFORE INSERT OR UPDATE
ON "layer_layer" FOR EACH ROW EXECUTE PROCEDURE
tsvector_update_trigger("ts_index", 'pg_catalog.spanish', title, abstract, categories_string);

/*
Trigger que llena el campo ts_index antes de un insert o update
en la tabla timeSeries_variable
*/
CREATE TRIGGER tsvector_update_variable BEFORE INSERT OR UPDATE
ON "timeSeries_variable" FOR EACH ROW EXECUTE PROCEDURE
tsvector_update_trigger("ts_index", 'pg_catalog.spanish', name, categories_string);

/*
Funcion para ingresar una medicion
Se valida que esa medicion no exista
*/
CREATE OR REPLACE FUNCTION InsertMeasurements
(idStation INTEGER, ts_in TIMESTAMP,readings JSON)
RETURNS void AS $$
BEGIN
	IF NOT(EXISTS(SELECT * FROM "timeSeries_measurement"
		WHERE "idStation_id"=idStation and "ts"=ts_in))
	THEN
		INSERT INTO "timeSeries_measurement"("idStation_id","ts","readings")
		VALUES(idStation,ts_in,readings);
	END IF;
END;
$$ LANGUAGE plpgsql;

