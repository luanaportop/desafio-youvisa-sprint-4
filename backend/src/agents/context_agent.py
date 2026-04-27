def build_context(status_data: dict) -> str:
    status_global = status_data.get("status_global", "DESCONHECIDO")
    documentos_faltando = status_data.get("tipos_faltando", [])

    return f"""
    Status global do processo: {status_global}
    Documentos faltando: {', '.join(documentos_faltando) if documentos_faltando else 'Nenhum'}
    """