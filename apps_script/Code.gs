const INTAKE_API_URL = 'https://YOUR-RENDER-APP.onrender.com/ingest';
const INTAKE_TOKEN = 'CHANGE_ME_TO_THE_SAME_VALUE_AS_INTAKE_TOKEN';

function onFormSubmit(e) {
  const named = e.namedValues;

  const name = getValue_(named, 'Name');
  const email = getValue_(named, 'Email');
  const phone = getValue_(named, 'Phone');
  const roleApplied = getValue_(named, 'Role Applied');
  const resumeText = getValue_(named, 'Resume Text');
  const resumeUpload = getValue_(named, 'Resume Upload');

  const payload = {
    name: name,
    email: email,
    phone: phone,
    role_applied: roleApplied,
    resume_text: resumeText,
    source: 'google-form'
  };

  if (!payload.resume_text && resumeUpload) {
    const fileId = extractDriveFileId_(resumeUpload);
    if (fileId) {
      const blob = DriveApp.getFileById(fileId).getBlob();
      payload.resume_pdf_base64 = Utilities.base64Encode(blob.getBytes());
    }
  }

  const response = UrlFetchApp.fetch(INTAKE_API_URL, {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'X-Intake-Token': INTAKE_TOKEN
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  });

  const result = JSON.parse(response.getContentText());
  const sheet = SpreadsheetApp.getActiveSheet();
  const row = e.range.getRow();
  writeHeaderIfMissing_(sheet);
  sheet.getRange(row, findColumn_(sheet, 'Candidate ID')).setValue(result.candidate_id || '');
  sheet.getRange(row, findColumn_(sheet, 'ATS Score')).setValue(result.ats_score || '');
  sheet.getRange(row, findColumn_(sheet, 'Active Until')).setValue(result.expires_at || '');
  sheet.getRange(row, findColumn_(sheet, 'Pinecone Synced')).setValue(result.pinecone_synced === true ? 'Yes' : 'No');
}

function getValue_(named, key) {
  return named[key] && named[key][0] ? String(named[key][0]).trim() : '';
}

function extractDriveFileId_(value) {
  const match = String(value).match(/[-\w]{25,}/);
  return match ? match[0] : '';
}

function writeHeaderIfMissing_(sheet) {
  const headers = ['Candidate ID', 'ATS Score', 'Active Until', 'Pinecone Synced'];
  headers.forEach(function(header) {
    if (findColumn_(sheet, header) === -1) {
      sheet.getRange(1, sheet.getLastColumn() + 1).setValue(header);
    }
  });
}

function findColumn_(sheet, header) {
  const values = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  for (let i = 0; i < values.length; i++) {
    if (String(values[i]).trim() === header) {
      return i + 1;
    }
  }
  return -1;
}
