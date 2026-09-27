/**
 * Extract a human-readable error message from any thrown value.
 * Handles Error objects, strings, and plain objects with message/error fields.
 * @param {*} error — caught exception value
 * @returns {string} best-effort error description
 */
export function describeError(error) {
  if (!error) return 'Unknown initialization error';
  if (error instanceof Error) {
    if (error.message && error.message.trim()) return error.message.trim();
    return error.name || 'Initialization error';
  }
  if (typeof error === 'string' && error.trim()) return error.trim();
  const serialized = serializeThrown(error);
  if (serialized) return serialized;
  return String(error);
}

/**
 * JSON/string detail for a thrown value. Cesium's default render panel does
 * `error.toString()` + `error.stack`, which becomes `[object Object]` /
 * `undefined` when the throw is a plain object. Always prefer this.
 * @param {*} value
 * @returns {string}
 */
export function serializeThrown(value) {
  if (value == null) return '';
  if (typeof value === 'string') return value.trim();
  if (value instanceof Error) {
    const parts = [value.name, value.message].filter((part) => String(part || '').trim());
    return parts.join(': ') || value.toString();
  }
  if (typeof value === 'object') {
    const maybeMessage = String(value.message || value.error || value.reason || '').trim();
    if (maybeMessage && maybeMessage !== '[object Object]') return maybeMessage;
    try {
      const serialized = JSON.stringify(value, serializeThrownReplacer);
      if (serialized && serialized !== '{}') return serialized;
    } catch {
      // cyclic / BigInt — fall through
    }
    const ctor = value.constructor?.name;
    if (ctor && ctor !== 'Object') return `${ctor}`;
  }
  const text = String(value);
  return text === '[object Object]' ? '' : text;
}

function serializeThrownReplacer(_key, nested) {
  if (typeof nested === 'bigint') return String(nested);
  if (nested instanceof Error) {
    return { name: nested.name, message: nested.message, stack: nested.stack };
  }
  return nested;
}

/**
 * Coerce any thrown value into a real Error so Cesium's render panel and
 * `console.error` show a message and stack instead of `[object Object]`.
 * @param {*} value
 * @param {string} [context]
 * @returns {Error}
 */
export function toError(value, context = '') {
  if (value instanceof Error) return value;
  const detail = serializeThrown(value) || 'non-Error throw';
  const prefix = context ? `${context}: ` : '';
  const error = new Error(`${prefix}${detail}`);
  error.name = 'WrappedThrow';
  error.cause = value;
  error.details = detail;
  return error;
}
