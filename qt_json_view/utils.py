import os
import cPickle as pickle
import json


class JsonReadError(Exception):
    pass


class JsonDumpError(Exception):
    pass


class PickleReadError(Exception):
    pass


class PickleDumpError(Exception):
    pass


def load(filepath, format="json", logger=None):
    """Load serialized data using the desired format"""
    errs = []
    data = None
    if os.path.isfile(filepath):
        try:
            with open(filepath, "r") as f:
                txt = f.read()
                try:
                    if format == "json":
                        data = json.loads(txt)
                    elif format == "pickle":
                        data = pickle.loads(txt)
                except:
                    errs.append("Ensure file format is "
                                "compatible with {}".format(
                                    format))
                else:
                    if logger:
                        logger.info(
                            "{} file loaded: {}".format(
                                format, filepath))
        except IOError:
            errs.append("Could not open {}: \"{}\"".format(
                format, filepath))
    else:
        errs.append("{} file not found: \"{}\"".format(
            format, filepath))

    if errs:
        if logger:
            logger.error("\n".join(errs))
            return {}
        else:
            if format == "json":
                raise JsonReadError("\n".join(errs))
            elif format == "pickle":
                raise PickleReadError("\n".join(errs))

    return data


def dump(data, filepath, format="json", logger=None, **kwargs):
    """Serialize data using the desired format"""
    errs = []
    content = None
    try:
        with open(filepath, "w") as f:
            try:
                if format == "json":
                    content = json.dumps(data, **kwargs)
                elif format == "pickle":
                    content = pickle.dumps(data, **kwargs)
                f.write(content)
            except:
                errs.append("Ensure data format is "
                            "compatible with {}".format(
                                format))
            else:
                if logger:
                    logger.info("{} saved to: {}".format(
                        format, filepath))
    except IOError:
        errs.append("Could not open {}: \"{}\"".format(
            format, filepath))

    if errs:
        if logger:
            logger.error("\n".join(errs))
            return {}
        else:
            if format == "json":
                raise JsonDumpError("\n".join(errs))
            elif format == "pickle":
                raise PickleDumpError("\n".join(errs))

    return content
