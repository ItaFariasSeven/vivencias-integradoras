const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);

    if (parts.length === 2){
        return parts.pop().split(';').shift();
    }
    return null
}

export async function prepararCsrf() {
  const response = await fetch(
    `${API_URL}/auth/csrf/`,
    {
      credentials: "include",
    }
  );

  if (!response.ok) {
    throw new Error(
      "Não foi possível preparar o CSRF."
    );
  }

  return response.json();
}

export async function apiFetch(
  caminho,
  options = {}
) {
  const method = (
    options.method || "GET"
  ).toUpperCase();

  const precisaCsrf = ![
    "GET",
    "HEAD",
    "OPTIONS",
    "TRACE",
  ].includes(method);

  if (
    precisaCsrf &&
    !getCookie("csrftoken")
  ) {
    await prepararCsrf();
  }

  const headers = new Headers(
    options.headers || {}
  );

  if (
    options.body &&
    !(options.body instanceof FormData) &&
    !headers.has("Content-Type")
  ) {
    headers.set(
      "Content-Type",
      "application/json"
    );
  }

  if (precisaCsrf) {
    const csrfToken =
      getCookie("csrftoken");

    if (csrfToken) {
      headers.set(
        "X-CSRFToken",
        csrfToken
      );
    }
  }

  const response = await fetch(
    `${API_URL}${caminho}`,
    {
      ...options,
      headers,
      credentials: "include",
    }
  );

  const contentType =
    response.headers.get(
      "content-type"
    ) || "";

  let dados;

  if (
    contentType.includes(
      "application/json"
    )
  ) {
    dados = await response.json();
  } else {
    dados = await response.text();
  }

  if (!response.ok) {
    const erro = new Error(
      dados?.erro ||
      dados?.detail ||
      "Erro na comunicação com o servidor."
    );

    erro.status = response.status;
    erro.data = dados;

    throw erro;
  }

  return dados;
}