# SPDX-License-Identifier: MIT OR Apache-2.0
# SPDX-FileCopyrightText: The Coding Guidelines Subcommittee Contributors

from sphinx.errors import SphinxError
from sphinx_needs.data import SphinxNeedsData
import logging

logger = logging.getLogger('sphinx')

class IntegrityCheckError(SphinxError):
    category = "Integrity Check Error"

def validate_required_fields(app, env):
    """

    """
    logger.debug("Validating required fields")
    data = SphinxNeedsData(env)
    needs = data.get_needs_view()

    required_fields = app.config.required_guideline_fields  # Access the configured values

    for key, value in needs.items():
        if value.get('type') == 'guideline': # other types include rationale, non_compliant_example, compliant_example 
            missing_fields = []
            for field in required_fields:
                if not value.get(field):
                    missing_fields.append(field)
            if missing_fields:
                error_message = (
                    f"Guideline '{value.get('title')}' (ID: {value.get('id')}) "
                    f"in {value.get('docname')}:{value.get('lineno')} is missing the following required fields: "
                    f"{', '.join(missing_fields)}"
                )
                logger.error(error_message)
                app.builder.statuscode = 1
                # exit(0)
                raise IntegrityCheckError(error_message) 
            logger.info("No missing required field")

            ####### 
            # need_id = value.get('id')
            # status = value.get('status')
            # release = value.get('release')
            # fls = value.get('fls')
            # decidability = value.get('decidability')
            # scope = value.get('scope')
            # tags = value.get('tags')
            #
            # print(f"Guideline Need ID: {key}")
            # print(f"  ID: {need_id}")
            # print(f"  Status: {status}")
            # print(f"  Release: {release}")
            # print(f"  FLS: {fls}")
            # print(f"  Decidability: {decidability}")
            # print(f"  Scope: {scope}")
            # print(f"  Tags: {tags}")
            # print("=============================")


