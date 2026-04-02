-- BigQuery does not enforce primary keys natively.
-- The id field is INT64 and is assigned by the application
-- using a SELECT MAX(id) + 1 pattern at insert time.

CREATE TABLE IF NOT EXISTS `suggestion_box.suggestions` (
  id         INT64     NOT NULL,
  category   STRING    NOT NULL,  -- one of: 'Facilities', 'Technology', 'General'
  message    STRING    NOT NULL,
  created_at TIMESTAMP NOT NULL
);
