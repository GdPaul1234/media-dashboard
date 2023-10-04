from typing import Optional
from pathlib import Path
from pydantic import BaseModel
from pydantic.types import DirectoryPath, FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict


class PathSettings(BaseModel):
    movies_folder: DirectoryPath
    series_folder: DirectoryPath
    title_strategies: Optional[FilePath] = None
    title_re_blacklist: Optional[FilePath] = None


class MediaDatabaseSettings(BaseModel):
    db_path: Path
    clean_after_update: bool = True


class LoggerSettings(BaseModel):
    file_path: FilePath


class Settings(BaseSettings):
    Paths: PathSettings
    MediaDatabase: Optional[MediaDatabaseSettings] = None
    Logger: Optional[LoggerSettings] = None

    model_config = SettingsConfigDict(env_nested_delimiter='__')
