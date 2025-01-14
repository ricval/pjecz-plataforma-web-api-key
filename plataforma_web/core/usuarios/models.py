"""
Usuarios, modelos
"""
from collections import OrderedDict

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin

from ..permisos.models import Permiso


class Usuario(Base, UniversalMixin):
    """Usuario"""

    WORKSPACES = OrderedDict(
        [
            ("BUSINESS STARTED", "Business Started"),
            ("BUSINESS STANDARD", "Business Standard"),
            ("COAHUILA", "Coahuila"),
            ("EXTERNO", "Externo"),
        ]
    )

    # Nombre de la tabla
    __tablename__ = "usuarios"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Claves foráneas
    autoridad_id = Column(Integer, ForeignKey("autoridades.id"), index=True, nullable=False)
    autoridad = relationship("Autoridad", back_populates="usuarios")
    oficina_id = Column(Integer, ForeignKey("oficinas.id"), index=True, nullable=False)
    oficina = relationship("Oficina", back_populates="usuarios")

    # Columnas
    email = Column(String(256), nullable=False, unique=True, index=True)
    nombres = Column(String(256), nullable=False)
    apellido_paterno = Column(String(256), nullable=False)
    apellido_materno = Column(String(256))
    curp = Column(String(18))
    puesto = Column(String(256))
    telefono = Column(String(48), nullable=False)
    extension = Column(String(24), nullable=False)
    workspace = Column(
        Enum(*WORKSPACES, name="tipos_workspaces", native_enum=False),
        index=True,
        nullable=False,
    )

    # Columnas que no deben ser expuestas
    api_key = Column(String(128), nullable=False)
    api_key_expiracion = Column(DateTime(), nullable=False)
    contrasena = Column(String(256), nullable=False)

    # Hijos
    arc_solicitudes_asignadas = relationship("ArcSolicitud", back_populates="usuario_asignado")
    arc_remesas_asignadas = relationship("ArcRemesa", back_populates="usuario_asignado")
    bitacoras = relationship("Bitacora", back_populates="usuario")
    entradas_salidas = relationship("EntradaSalida", back_populates="usuario")
    inv_custodias = relationship("InvCustodia", back_populates="usuario")
    usuarios_roles = relationship("UsuarioRol", back_populates="usuario")

    # Propiedades
    permisos_consultados = {}

    @property
    def nombre(self):
        """Junta nombres, apellido_paterno y apellido materno"""
        return self.nombres + " " + self.apellido_paterno + " " + self.apellido_materno

    @property
    def distrito_id(self):
        """Distrito ID"""
        return self.autoridad.distrito_id

    @property
    def distrito_clave(self):
        """Distrito clave"""
        return self.autoridad.distrito.clave

    @property
    def distrito_nombre(self):
        """Distrito nombre"""
        return self.autoridad.distrito.nombre

    @property
    def distrito_nombre_corto(self):
        """Distrito nombre corto"""
        return self.autoridad.distrito.nombre_corto

    @property
    def autoridad_clave(self):
        """Autoridad clave"""
        return self.autoridad.clave

    @property
    def autoridad_descripcion(self):
        """Autoridad descripción"""
        return self.autoridad.descripcion

    @property
    def autoridad_descripcion_corta(self):
        """Autoridad descripción corta"""
        return self.autoridad.descripcion_corta

    @property
    def oficina_clave(self):
        """Oficina clave"""
        return self.oficina.clave

    @property
    def permissions(self):
        """Entrega un diccionario con todos los permisos"""
        if len(self.permisos_consultados) > 0:
            return self.permisos_consultados
        self.permisos_consultados = {}
        for usuario_rol in self.usuarios_roles:
            if usuario_rol.estatus == "A":
                for permiso in usuario_rol.rol.permisos:
                    if permiso.estatus == "A":
                        etiqueta = permiso.modulo.nombre
                        if etiqueta not in self.permisos_consultados or permiso.nivel > self.permisos_consultados[etiqueta]:
                            self.permisos_consultados[etiqueta] = permiso.nivel
        return self.permisos_consultados

    def can(self, modulo_nombre: str, permission: int):
        """¿Tiene permiso?"""
        if modulo_nombre in self.permisos:
            return self.permisos[modulo_nombre] >= permission
        return False

    def can_view(self, modulo_nombre: str):
        """¿Tiene permiso para ver?"""
        return self.can(modulo_nombre, Permiso.VER)

    def can_edit(self, modulo_nombre: str):
        """¿Tiene permiso para editar?"""
        return self.can(modulo_nombre, Permiso.MODIFICAR)

    def can_insert(self, modulo_nombre: str):
        """¿Tiene permiso para agregar?"""
        return self.can(modulo_nombre, Permiso.CREAR)

    def can_admin(self, modulo_nombre: str):
        """¿Tiene permiso para administrar?"""
        return self.can(modulo_nombre, Permiso.ADMINISTRAR)

    def __repr__(self):
        """Representación"""
        return f"<Usuario {self.email}>"
