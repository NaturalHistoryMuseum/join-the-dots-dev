export default function fieldNameCalc(db_name) {
  const words = db_name.split('_');
  const capitalised = words.map(
    (word) => word.charAt(0).toUpperCase() + word.slice(1),
  );
  const string = capitalised.join(' ');
  return string;
}
