CREATE TABLE IF NOT EXISTS `suggestion_box.suggestions` (
  id         STRING    NOT NULL,
  category   STRING    NOT NULL,  -- one of: 'Facilities', 'Technology', 'General'
  message    STRING    NOT NULL,
  created_at TIMESTAMP NOT NULL
);
