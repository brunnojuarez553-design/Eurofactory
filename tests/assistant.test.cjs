/* Pruebas sin API key ni conexión: node --test tests/assistant.test.cjs */
'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');
const { URL } = require('node:url');

const handler = require(path.resolve(__dirname, '../api/assistant.js'));
const originalFetch = global.fetch;
const oldApiKey = process.env.GROQ_API_KEY;
const oldModel = process.env.GROQ_MODEL;

function response() {
  return {
    statusCode: 200, headers: {}, payload: null,
    setHeader(name, val) { this.headers[name] = val; },
    end(serialized) { this.payload = JSON.parse(serialized); },
  };
}
async function request(message, options = {}) {
  const resp = response();
  await handler({
    method: options.method || 'POST',
    headers: {
      host: 'eurofactory.vercel.app',
      origin: 'https://eurofactory.vercel.app',
      'content-type': 'application/json',
      'x-real-ip': '198.51.100.' + (options.ip || '10'),
    },
    body: { message, history: [], lead: {}, ...options.body },
  }, resp);
  return resp;
}
function groqReply(data) {
  return {
    ok: true, status: 200,
    json: async () => ({
      choices: [{ message: { content: JSON.stringify(data) } }],
    }),
  };
}

test('asistente: Groq vigente, saludo único, schema y WhatsApp por sede', async t => {
  process.env.GROQ_API_KEY = 'test-only-not-a-secret';
  process.env.GROQ_MODEL = 'llama-3.3-70b-versatile';
  let calls = [];
  global.fetch = async (_, opts) => {
    calls.push(JSON.parse(opts.body));
    return groqReply({
      reply: '¡Hola! Bienvenido a Euro Factory. Perfecto, ya podemos preparar tu solicitud.',
      updates: { branch: 'valencia', name: 'Cliente de prueba', vehicle: 'BMW 320i 2017',
        service: 'Diagnóstico', date: 'El lunes', phone: null },
      wantsAppointment: true,
    });
  };

  await t.test('solo hola no devuelve otro saludo ni consume token', async () => {
    const r = await request(' ¡Hola! ', { ip: '11' });
    assert.equal(r.statusCode, 200);
    assert.match(r.payload.reply, /^Contame /);
    assert.equal(calls.length, 0);
  });
  await t.test('modelo obsoleto se reemplaza por GPT-OSS y respuesta sin bienvenida', async () => {
    const r = await request('Soy un cliente, deseo una cita para el diagnóstico de mi BMW el lunes en Valencia', { ip: '12' });
    assert.equal(r.statusCode, 200);
    assert.equal(calls[0].model, 'openai/gpt-oss-120b');
    assert.equal(calls[0].response_format.type, 'json_schema');
    assert.equal(calls[0].response_format.json_schema.strict, true);
    assert.equal(calls[0].messages[1].role, 'assistant'); // la bienvenida ya se mostró en pantalla
    assert.doesNotMatch(r.payload.reply, /^hola|^bienvenid/i);
    assert.equal(r.payload.ready, true);
    const wa = new URL(r.payload.whatsapp.url);
    assert.equal(wa.host, 'wa.me');
    assert.equal(wa.pathname, '/584144630453');
    const text = wa.searchParams.get('text');
    for (const part of ['Valencia', 'BMW 320i 2017', 'Cliente de prueba', 'Diagnóstico', 'El lunes'])
      assert.ok(text.includes(part), 'Falta ' + part);
  });
  await t.test('una conversación sin cita no muestra el botón', async () => {
    global.fetch = async () => groqReply({
      reply: 'Claro, atendemos diagnóstico computarizado.',
      updates: { branch: null, name: null, vehicle: null, service: null, date: null, phone: null },
      wantsAppointment: false,
    });
    const r = await request('¿Qué servicios ofrecen?', { ip: '13' });
    assert.equal(r.payload.ready, false);
    assert.equal(r.payload.whatsapp, null);
  });
  await t.test('errores de credenciales tienen respuesta útil, sin exponer key', async () => {
    global.fetch = async () => ({ ok: false, status: 401 });
    const r = await request('¿Qué servicios tienen?', { ip: '14' });
    assert.equal(r.statusCode, 502);
    assert.match(r.payload.error, /clave|permisos/i);
    assert.doesNotMatch(JSON.stringify(r.payload), /test-only-not-a-secret/);
  });
});
process.on('exit', () => {
  global.fetch = originalFetch;
  if (oldApiKey === undefined) delete process.env.GROQ_API_KEY;
  else process.env.GROQ_API_KEY = oldApiKey;
  if (oldModel === undefined) delete process.env.GROQ_MODEL;
  else process.env.GROQ_MODEL = oldModel;
});
