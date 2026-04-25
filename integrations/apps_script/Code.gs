// GrappleCoach — Google Apps Script webhook
// Deploy as Web App (Execute as: Me, Who has access: Anyone)

var SPREADSHEET_ID = ''; // Paste your spreadsheet ID here, or leave blank to use the bound spreadsheet
var SHEET_NAME = 'Entrenamientos';
var HEADERS = ['Fecha', 'Usuario', 'Ejercicio', 'Series', 'Reps', 'Carga (kg)', 'Duración (min)', 'Observaciones', 'Timestamp'];

// ─── Main handler ────────────────────────────────────────────────────────────

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    if (data.modo === 'registro') return handleRegistro(data);
    if (data.modo === 'consulta') return handleConsulta(data);
    return jsonResponse({ ok: false, error: 'Modo inválido. Usá "registro" o "consulta".' });
  } catch (err) {
    return jsonResponse({ ok: false, error: err.message });
  }
}

// ─── Handlers ────────────────────────────────────────────────────────────────

function handleRegistro(data) {
  var required = ['usuario', 'fecha', 'ejercicio', 'series', 'repeticiones', 'carga_kg'];
  for (var i = 0; i < required.length; i++) {
    if (data[required[i]] == null) {
      return jsonResponse({ ok: false, error: 'Falta campo obligatorio: ' + required[i] });
    }
  }

  var sheet = getOrCreateSheet();
  sheet.appendRow([
    data.fecha,
    data.usuario,
    data.ejercicio,
    data.series,
    data.repeticiones,
    data.carga_kg,
    data.duracion_min || '',
    data.observaciones || '',
    new Date().toISOString()
  ]);

  return jsonResponse({ ok: true, mensaje: 'Sesión registrada correctamente.' });
}

function handleConsulta(data) {
  if (!data.usuario) {
    return jsonResponse({ ok: false, error: 'Falta campo obligatorio: usuario' });
  }

  var sheet = getOrCreateSheet();
  var rows = sheet.getDataRange().getValues();

  var cutoff = null;
  if (data.rango_dias) {
    cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - Number(data.rango_dias));
  }

  // Skip header row (index 0)
  var registros = rows.slice(1).filter(function(row) {
    if (row[1] !== data.usuario) return false;
    if (data.ejercicio && row[2] !== data.ejercicio) return false;
    if (cutoff && new Date(row[0]) < cutoff) return false;
    return true;
  }).map(function(row) {
    return {
      fecha:        row[0],
      usuario:      row[1],
      ejercicio:    row[2],
      series:       row[3],
      repeticiones: row[4],
      carga_kg:     row[5],
      duracion_min: row[6],
      observaciones:row[7]
    };
  });

  return jsonResponse({ ok: true, registros: registros });
}

// ─── Sheet helper ─────────────────────────────────────────────────────────────

function getOrCreateSheet() {
  var ss = SPREADSHEET_ID
    ? SpreadsheetApp.openById(SPREADSHEET_ID)
    : SpreadsheetApp.getActiveSpreadsheet();

  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    var headerRange = sheet.getRange(1, 1, 1, HEADERS.length);
    headerRange.setValues([HEADERS]);
    headerRange.setFontWeight('bold');
    headerRange.setBackground('#f3f3f3');
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function jsonResponse(obj) {
  var output = ContentService.createTextOutput(JSON.stringify(obj));
  output.setMimeType(ContentService.MimeType.JSON);
  return output;
}

// ─── Test helpers (run from the Apps Script editor) ──────────────────────────

function testRegistro() {
  var result = doPost({
    postData: {
      contents: JSON.stringify({
        modo:          'registro',
        usuario:       'TestAthlete',
        fecha:         '2026-04-25',
        ejercicio:     'Sentadilla trasera',
        series:        5,
        repeticiones:  5,
        carga_kg:      100,
        duracion_min:  45,
        observaciones: 'Test desde el editor'
      })
    }
  });
  Logger.log(result.getContent());
}

function testConsulta() {
  var result = doPost({
    postData: {
      contents: JSON.stringify({
        modo:       'consulta',
        usuario:    'TestAthlete',
        rango_dias: 30
      })
    }
  });
  Logger.log(result.getContent());
}
