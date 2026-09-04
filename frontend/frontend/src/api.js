const API_BASE_URL = "http://127.0.0.1:8000";

export const getMediaUrl = (path) => {
  if (!path) return "";
  if (path.startsWith("http://") || path.startsWith("https://")) return path;
  const cleanPath = path.startsWith("/") ? path : `/${path}`;
  return `${API_BASE_URL}${cleanPath}`;
};

export const checkHealth = async () => {
  try {
    const res = await fetch(`${API_BASE_URL}/`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return await res.json();
  } catch (err) {
    return { status: "offline", error: err.message };
  }
};

export const ingestFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE_URL}/ingest`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || `Ingestion failed with status ${res.status}`);
  }

  return await res.json();
};

export const sendChatQuery = async ({ query, sessionId = null, topK = 5, scoreThreshold = 0.0 }) => {
  const res = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query,
      session_id: sessionId,
      top_k: topK,
      score_threshold: scoreThreshold,
    }),
  });

  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || `Chat query failed with status ${res.status}`);
  }

  return await res.json();
};

export const fetchDocuments = async () => {
  const res = await fetch(`${API_BASE_URL}/documents`);
  if (!res.ok) {
    throw new Error(`Failed to fetch documents (${res.status})`);
  }
  const data = await res.json();
  return data.documents || [];
};

export const deleteDocument = async (documentId) => {
  const res = await fetch(`${API_BASE_URL}/documents/${documentId}`, {
    method: "DELETE",
  });
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || `Failed to delete document (${res.status})`);
  }
  return await res.json();
};

export const fetchChatHistory = async (sessionId) => {
  if (!sessionId) return [];
  const res = await fetch(`${API_BASE_URL}/chat/history/${sessionId}`);
  if (!res.ok) return [];
  const data = await res.json();
  return data.history || [];
};

export const clearChatHistory = async (sessionId) => {
  if (!sessionId) return true;
  const res = await fetch(`${API_BASE_URL}/chat/history/${sessionId}`, {
    method: "DELETE",
  });
  return res.ok;
};
