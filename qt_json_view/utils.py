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


def load(filepath, encoding="json", logger=None):
    """Load serialized data using the desired encoding"""
    errs = []
    data = None
    if os.path.isfile(filepath):
        try:
            with open(filepath, "r") as f:
                txt = f.read()
                try:
                    if encoding == "json":
                        data = json.loads(txt)
                    elif encoding == "pickle":
                        data = pickle.loads(txt)
                except:
                    errs.append("Ensure file format is "
                                "compatible with {}".format(
                                    encoding))
                else:
                    if logger:
                        logger.info(
                            "{} file loaded: {}".format(
                                encoding, filepath))
        except IOError:
            errs.append("Could not open {}: \"{}\"".format(
                encoding, filepath))
    else:
        errs.append("{} file not found: \"{}\"".format(
            encoding, filepath))

    if errs:
        if logger:
            logger.error("\n".join(errs))
            return {}
        else:
            if encoding == "json":
                raise JsonReadError("\n".join(errs))
            elif encoding == "pickle":
                raise PickleReadError("\n".join(errs))

    return data


def dump(data, filepath, encoding="json", logger=None):
    """Serialize data using the desired encoding"""
    errs = []
    content = None
    try:
        with open(filepath, "w") as f:
            try:
                if encoding == "json":
                    content = json.dumps(data)
                elif encoding == "pickle":
                    content = pickle.dumps(data)
                f.write(content)
            except:
                errs.append("Ensure data format is "
                            "compatible with {}".format(
                                encoding))
            else:
                if logger:
                    logger.info("{} saved to: {}".format(
                        encoding, filepath))
    except IOError:
        errs.append("Could not open {}: \"{}\"".format(
            encoding, filepath))

    if errs:
        if logger:
            logger.error("\n".join(errs))
            return {}
        else:
            if encoding == "json":
                raise JsonDumpError("\n".join(errs))
            elif encoding == "pickle":
                raise PickleDumpError("\n".join(errs))

    return content
