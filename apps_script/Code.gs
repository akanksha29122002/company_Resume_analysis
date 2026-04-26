const API_BASE_URL = 'https://YOUR-RENDER-APP.onrender.com';
const INTAKE_TOKEN = 'CHANGE_ME_TO_THE_SAME_VALUE_AS_INTAKE_TOKEN';

function onCandidateFormSubmit(e) {
  const named = e.namedValues;

  const payload = {
    name: getValue_(named, 'Name'),
    email: getValue_(named, 'Email'),
    phone: getValue_(named, 'Phone'),
    role_applied: getValue_(named, 'Role Applied'),
    resume_text: getValue_(named, 'Resume Text'),
    job_description: getValue_(named, 'Job Description'),
    source: 'candidate-google-form'
  };

  const resumeUpload = getValue_(named, 'Resume Upload');
  if (!payload.resume_text && resumeUpload) {
    payload.resume_pdf_base64 = readDriveFileAsBase64_(resumeUpload);
  }

  const result = postJson_('/ingest', payload);
  const row = e.range.getRow();
  const sheet = SpreadsheetApp.getActiveSheet();
  writeHeaders_(sheet, ['Candidate ID', 'ATS Score', 'Active Until', 'Pinecone Synced']);
  setCell_(sheet, row, 'Candidate ID', result.candidate_id || '');
  setCell_(sheet, row, 'ATS Score', result.ats_score || '');
  setCell_(sheet, row, 'Active Until', result.expires_at || '');
  setCell_(sheet, row, 'Pinecone Synced', result.pinecone_synced === true ? 'Yes' : 'No');
}

function onCompanyFormSubmit(e) {
  const named = e.namedValues;

  const payload = {
    company_name: getValue_(named, 'Company Name'),
    record_type: getValue_(named, 'Record Type') || 'Requirement',
    title: getValue_(named, 'Title'),
    date_or_period: getValue_(named, 'Date or Period'),
    details: getValue_(named, 'Details'),
    tags: getValue_(named, 'Tags'),
    source: 'company-google-form'
  };

  const documentUpload = getValue_(named, 'Company Document Upload');
  if (documentUpload) {
    payload.document_pdf_base64 = readDriveFileAsBase64_(documentUpload);
  }

  const result = postJson_('/company-ingest', payload);
  const row = e.range.getRow();
  const sheet = SpreadsheetApp.getActiveSheet();
  writeHeaders_(sheet, ['Company Record ID', 'Active Until', 'Pinecone Synced']);
  setCell_(sheet, row, 'Company Record ID', result.record_id || '');
  setCell_(sheet, row, 'Active Until', result.expires_at || '');
  setCell_(sheet, row, 'Pinecone Synced', result.pinecone_synced === true ? 'Yes' : 'No');
}

function calculateIdealMatches() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const requirement = Browser.inputBox('Paste company requirement for automatic RAG matching');
  if (!requirement || requirement === 'cancel') {
    return;
  }

  const result = postJson_('/rag-match', {
    requirement: requirement,
    limit: 10,
    use_pinecone: true
  });

  writeHeaders_(sheet, ['RAG Answer', 'Best Candidate', 'Potential', 'Match Score', 'Recommendation']);
  const row = Math.max(sheet.getLastRow() + 1, 2);
  const best = result.best_candidate || {};
  setCell_(sheet, row, 'RAG Answer', result.answer || '');
  setCell_(sheet, row, 'Best Candidate', best.name || '');
  setCell_(sheet, row, 'Potential', best.potential || '');
  setCell_(sheet, row, 'Match Score', best.match_score || '');
  setCell_(sheet, row, 'Recommendation', best.recommendation || '');
}

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Resume RAG')
    .addItem('Calculate ideal matches', 'calculateIdealMatches')
    .addToUi();
}

function postJson_(path, payload) {
  const response = UrlFetchApp.fetch(API_BASE_URL + path, {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'X-Intake-Token': INTAKE_TOKEN
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  });

  const status = response.getResponseCode();
  const body = response.getContentText();
  if (status < 200 || status >= 300) {
    throw new Error('API error ' + status + ': ' + body);
  }
  return JSON.parse(body);
}

function readDriveFileAsBase64_(value) {
  const fileId = extractDriveFileId_(value);
  if (!fileId) {
    return '';
  }
  const blob = DriveApp.getFileById(fileId).getBlob();
  return Utilities.base64Encode(blob.getBytes());
}

function getValue_(named, key) {
  return named[key] && named[key][0] ? String(named[key][0]).trim() : '';
}

function extractDriveFileId_(value) {
  const match = String(value).match(/[-\w]{25,}/);
  return match ? match[0] : '';
}

function writeHeaders_(sheet, headers) {
  headers.forEach(function(header) {
    if (findColumn_(sheet, header) === -1) {
      sheet.getRange(1, sheet.getLastColumn() + 1).setValue(header);
    }
  });
}

function setCell_(sheet, row, header, value) {
  const column = findColumn_(sheet, header);
  if (column !== -1) {
    sheet.getRange(row, column).setValue(value);
  }
}

function findColumn_(sheet, header) {
  const lastColumn = Math.max(sheet.getLastColumn(), 1);
  const values = sheet.getRange(1, 1, 1, lastColumn).getValues()[0];
  for (let i = 0; i < values.length; i++) {
    if (String(values[i]).trim() === header) {
      return i + 1;
    }
  }
  return -1;
}
