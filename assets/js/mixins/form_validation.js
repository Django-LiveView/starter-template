// Literal regular expressions that will be checked
export const patterns = {
  // Only letters (accents allowed) and spaces
  alphabeticCharacters: /^(?:(?=[^\d])[\w\s\-À-ÖØ-öø-ÿĀ-ū])+$/,
  /* Must have: @ . and a minimum of 2 characters after the dot.
   Can have: special characters and numbers too. */
  email: /^[-!#$%&'*+0-9=?A-Z^_a-z`{|}~](\\.?[-!#$%&'*+0-9=?A-Z^_a-z`{|}~])*@[a-zA-Z0-9](-*\\.?[a-zA-Z0-9])*\\.[a-zA-Z](-?[a-zA-Z0-9])+$/,
  // Phone prefix (maybe in brackets) allowed
  phone: /^[()+\s0-9]+$/
}

// Reusable functions. All of them will be returning true if the field is ready to be sent
/**
 *  Checking that the form field is filled in
 *
 * @param string Input value
 * @returns {boolean} True: the field is not empty
 */
export function fieldIsFilledIn(string) {
  return string?.trim().length > 0;
}

/**
 *  Checking that the form field has the correct format
 *
 * @param {RegExp} pattern Pattern to check
 * @param string Input value
 * @returns {boolean} True: the input value matches the pattern
 */
export function fieldHasRightPattern(pattern, string) {
  return pattern.test(string);
}

/**
 *  Checking that the field has a minimum of X characters
 *
 * @param string Input value
 * @param {number} minLength The chosen minimum length for the input
 * @returns {boolean} True: the field has the minimum length
 */
export function fieldHasMinLength(string, minLength) {
  return string?.trim().length >= minLength;
}
