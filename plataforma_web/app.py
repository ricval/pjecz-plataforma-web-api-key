"""
PJECZ Plataforma Web API Key
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from config.settings import get_settings

from .v3.abogados.paths import abogados
from .v3.arc_documentos.paths import arc_documentos
from .v3.arc_juzgados_extintos.paths import arc_juzgados_extintos
from .v3.arc_remesas.paths import arc_remesas
from .v3.arc_remesas_documentos.paths import arc_remesas_documentos
from .v3.arc_solicitudes.paths import arc_solicitudes
from .v3.audiencias.paths import audiencias
from .v3.autoridades.paths import autoridades
from .v3.bitacoras.paths import bitacoras
from .v3.boletines.paths import boletines
from .v3.centros_trabajos.paths import centros_trabajos
from .v3.cit_dias_inhabiles.paths import cit_dias_inhabiles
from .v3.distritos.paths import distritos
from .v3.domicilios.paths import domicilios
from .v3.edictos.paths import edictos
from .v3.entradas_salidas.paths import entradas_salidas
from .v3.epocas.paths import epocas
from .v3.funcionarios.paths import funcionarios
from .v3.glosas.paths import glosas
from .v3.inv_categorias.paths import inv_categorias
from .v3.inv_componentes.paths import inv_componentes
from .v3.inv_custodias.paths import inv_custodias
from .v3.inv_equipos.paths import inv_equipos
from .v3.inv_marcas.paths import inv_marcas
from .v3.inv_modelos.paths import inv_modelos
from .v3.inv_redes.paths import inv_redes
from .v3.listas_de_acuerdos.paths import listas_de_acuerdos
from .v3.materias.paths import materias
from .v3.materias_tipos_juicios.paths import materias_tipos_juicios
from .v3.modulos.paths import modulos
from .v3.oficinas.paths import oficinas
from .v3.peritos.paths import peritos
from .v3.peritos_tipos.paths import peritos_tipos
from .v3.permisos.paths import permisos
from .v3.redam.paths import redam
from .v3.repsvm_agresores.paths import repsvm_agresores
from .v3.roles.paths import roles
from .v3.sentencias.paths import sentencias
from .v3.siga_bitacoras.paths import siga_bitacoras
from .v3.siga_grabaciones.paths import siga_grabaciones
from .v3.siga_salas.paths import siga_salas
from .v3.tesis_jurisprudencias.paths import tesis_jurisprudencias
from .v3.ubicaciones_expedientes.paths import ubicaciones_expedientes
from .v3.usuarios.paths import usuarios
from .v3.usuarios_roles.paths import usuarios_roles


def create_app() -> FastAPI:
    """Crea la aplicación FastAPI"""

    # FastAPI
    app = FastAPI(
        title="PJECZ Plataforma Web API Key",
        description="Bienvenido a PJECZ Plataforma Web API Key. Esta API es para trabajar con los datos de Plataforma Web. Se requiere tener una api-key para usarse.",
        docs_url="/docs",
        redoc_url=None,
    )

    # CORSMiddleware
    settings = get_settings()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origins.split(","),
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Rutas
    app.include_router(abogados)
    app.include_router(arc_documentos)
    app.include_router(arc_juzgados_extintos)
    app.include_router(arc_remesas)
    app.include_router(arc_remesas_documentos)
    app.include_router(arc_solicitudes)
    app.include_router(audiencias)
    app.include_router(autoridades)
    app.include_router(bitacoras)
    app.include_router(boletines)
    app.include_router(centros_trabajos)
    app.include_router(cit_dias_inhabiles)
    app.include_router(distritos)
    app.include_router(domicilios)
    app.include_router(edictos)
    app.include_router(entradas_salidas)
    app.include_router(epocas)
    app.include_router(funcionarios)
    app.include_router(glosas)
    app.include_router(inv_categorias)
    app.include_router(inv_componentes)
    app.include_router(inv_custodias)
    app.include_router(inv_equipos)
    app.include_router(inv_marcas)
    app.include_router(inv_modelos)
    app.include_router(inv_redes)
    app.include_router(listas_de_acuerdos)
    app.include_router(materias)
    app.include_router(materias_tipos_juicios)
    app.include_router(modulos)
    app.include_router(oficinas)
    app.include_router(peritos)
    app.include_router(peritos_tipos)
    app.include_router(permisos)
    app.include_router(redam)
    app.include_router(repsvm_agresores)
    app.include_router(roles)
    app.include_router(sentencias)
    app.include_router(siga_bitacoras)
    app.include_router(siga_grabaciones)
    app.include_router(siga_salas)
    app.include_router(tesis_jurisprudencias)
    app.include_router(usuarios)
    app.include_router(usuarios_roles)
    app.include_router(ubicaciones_expedientes)

    # Paginación
    add_pagination(app)

    # Mensaje de Bienvenida
    @app.get("/")
    async def root():
        """Mensaje de Bienvenida"""
        return {"message": "Bienvenido a PJECZ Plataforma Web API Key. Esta API es para trabajar con los datos de Plataforma Web. Se requiere tener una api-key para usarse."}

    # Entregar
    return app
