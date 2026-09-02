export default function fieldNameCalc(db_name) {
  if (db_name) {
    const words = db_name.split('_');
    const capitalised = words.map(
      (word) => word.charAt(0).toUpperCase() + word.slice(1),
    );
    const string = capitalised.join(' ');
    return string;
  } else {
    return '';
  }
}

export const APP_ENV = import.meta.env.VITE_APP_ENV;
