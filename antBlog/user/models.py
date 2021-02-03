# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt


from antblog.database import Column, PkModel, db, reference_col, relationship
from antblog.extensions import bcrypt


class Role(PkModel):
    """A role for a user."""

    __tablename__ = "roles"
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col("users", nullable=True)
    user = relationship("User", backref="rose")

    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Role({self.name})>"


class User(PkModel):
    """A user of the app."""

    __tablename__ = "users"
    username = Column(db.String(80), unique=True, nullable=False)
    # email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    # password = Column(db.LargeBinary(128), nullable=True)
    hashed_password = db.Column(db.Text)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    active = Column(db.Boolean, default=True, server_default="true")
    is_admin = Column(db.Boolean(), default=False)

    roles = Column(db.Text)

    # def __init__(self, username, email, **kwargs):
    #     """Create instance."""
    #     super().__init__(username=username, email=email, **kwargs)
    # if password:
    #     self.set_password(password)
    # else:
    #     self.password = None

    # def set_password(self, password):
    #     """Set password."""
    #     self.password = bcrypt.generate_password_hash(password)

    # def check_password(self, value):
    #     """Check password."""
    #     return bcrypt.check_password_hash(self.password, value)

    # @property
    # def full_name(self):
    #     """Full user name."""
    #     return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"

    @property
    def identity(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has an ``identity`` instance
        attribute or property that provides the unique id of the user instance
        """
        return self.id

    @property
    def rolenames(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has a ``rolenames`` instance
        attribute or property that provides a list of strings that describe the roles
        attached to the user instance
        """
        try:
            return self.roles.split(",")
        except Exception:
            return []

    @property
    def password(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has a ``password`` instance
        attribute or property that provides the hashed password assigned to the user
        instance
        """
        return self.hashed_password

    @classmethod
    def lookup(cls, username):
        """
        *Required Method*

        flask-praetorian requires that the user class implements a ``lookup()``
        class method that takes a single ``username`` argument and returns a user
        instance if there is one that matches or ``None`` if there is not.
        """
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        """
        *Required Method*

        flask-praetorian requires that the user class implements an ``identify()``
        class method that takes a single ``id`` argument and returns user instance if
        there is one that matches or ``None`` if there is not.
        """
        return cls.query.get(id)

    def is_valid(self):
        return self.active
