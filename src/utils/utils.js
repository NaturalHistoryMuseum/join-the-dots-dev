export default function fieldNameCalc(db_name) {
  const words = db_name.split('_');
  const capitalised = words.map(
    (word) => word.charAt(0).toUpperCase() + word.slice(1),
  );
  const string = capitalised.join(' ');
  return string;
}

export async function getFieldHelpText(field_name) {
  const data = await import('../utils/field_tooltips.json');
  const field_tooltips = data.default || [];
  console.log(field_tooltips);
  const field_tooltip = field_tooltips.find(
    (field) => field.col_name === field_name,
  );
  console.log(field_tooltip);
  return field_tooltip ? field_tooltip.description : '';
}
